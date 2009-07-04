#
# sqlite.py - Ed Bartosh <bartosh@gmail.com>, <Peter.Bienstman@UGent.be>
#

import os
import shutil
import sqlite3
from datetime import datetime

from mnemosyne.libmnemosyne.fact import Fact
from mnemosyne.libmnemosyne.card import Card
from mnemosyne.libmnemosyne.database import Database
from mnemosyne.libmnemosyne.category import Category
from mnemosyne.libmnemosyne.fact_view import FactView
from mnemosyne.libmnemosyne.start_date import StartDate
from mnemosyne.libmnemosyne.exceptions import SaveError, LoadError
from mnemosyne.libmnemosyne.exceptions import PluginError, MissingPluginError
from mnemosyne.libmnemosyne.utils import expand_path, contract_path
from mnemosyne.libmnemosyne.component_manager import card_types, scheduler
from mnemosyne.libmnemosyne.component_manager import card_type_by_id
from mnemosyne.libmnemosyne.component_manager import component_manager
from mnemosyne.libmnemosyne.component_manager import config, log, plugins
from mnemosyne.libmnemosyne.component_manager import ui_controller_review

# Note: all id's beginning with an underscore refer to primary keys in the
# SQL database. All other id's correspond to the id's used in libmnemosyne.
# We don't use libmnemosyne id's as primary keys for speed reasons.

SCHEMA = """
    begin;
    
    create table facts(
        _id integer primary key,
        id text unique,
        card_type_id text,
        creation_date timestamp,
        modification_date timestamp,
        needs_sync boolean default 1
    );

    create table data_for_fact(
        _id integer primary key,
        _fact_id int,
        key text,
        value text
    );
    
    create table cards(
        _id integer primary key,
        id text unique,
        _fact_id int,
        fact_view_id int,
        grade int,
        easiness real,
        acq_reps int,
        ret_reps int,
        lapses int,
        acq_reps_since_lapse int,
        ret_reps_since_lapse int,
        last_rep real,
        next_rep real,
        unseen boolean default 1,
        extra_data text default "",
        seen_in_this_session int default 0,
        needs_sync boolean default 1,
        active boolean default 1,
        in_view boolean default 1
    );

    create table categories(
        _id integer primary key,
        _parent_key int default 0,
        id text unique,
        name text,
        needs_sync boolean default 1
    );

    create table categories_for_card(
        _id integer primary key,
        _category_id int,
        _card_id int
    );

    create table global_variables(
        key text,
        value text
    );
    
    commit;
"""


class SQLite(Database):

    version = "SQL 1.0"
    suffix = ".db"

    def __init__(self):
        self._connection = None
        self._path = None # Needed for lazy creation of connection.
        self.load_failed = False
        self.start_date = None

    @property
    def con(self):
        
        """Connection to the database, lazily created."""

        if not self._connection:
            self._connection = sqlite3.connect(self._path,
                detect_types = sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def new(self, path):
        if self.is_loaded():
            self.unload()
        self._path = expand_path(path, config().basedir)
        if os.path.exists(self._path):
            os.remove(self._path)
        self.load_failed = False      
        self.start_date = StartDate()
        self.con.executescript(SCHEMA) # Create tables.
        self.con.execute("insert into global_variables(key,value) values(?,?)",
                        ("start_date", datetime.strftime(self.start_date.start,
                         "%Y-%m-%d %H:%M:%S")))
        self.con.execute("insert into global_variables(key,value) values(?,?)",
                        ("version", self.version))
        self.con.commit()
        config()["path"] = self._path
        log().new_database()

    def load(self, path):
        if self.is_loaded():        
            self.unload()
        self._path = expand_path(path, config().basedir)
        try:
            sql_res = self.con.execute("""select value from global_variables
                where key=?""", ("start_date", )).fetchone()
            self.set_start_date(StartDate(datetime.strptime(sql_res["value"],
                "%Y-%m-%d %H:%M:%S")))
            self.load_failed = False
        except:
            self.load_failed = True
            raise LoadError

        # Check database version.
        sql_res = self.con.execute("""select value from global_variables
            where key=?""", ("version", )).fetchone()
        if sql_res["value"] != self.version:
            print "Warning: database version mismatch."
            self.load_failed = True
            raise LoadError

        # Vacuum database from time to time.
        # TODO: skip this on a mobile machine?

        config()["times_loaded"] = config()["times_loaded"] + 1
        if config()["times_loaded"] % 5 == 0:
            config()["times_loaded"] = 0
            self.con.execute("vacuum")

        # Deal with clones and plugins, also plugins for parent classes.
        plugin_needed = set()
        clone_needed = []
        active_id = set(card_type.id for card_type in card_types())
        for cursor in self.con.execute("select distinct card_type_id from facts"):
            id = cursor[0]
            while "." in id: # Move up one level of the hierarchy.
                id, child_name = id.rsplit(".", 1)          
                if id.endswith("_CLONED"):
                    id = id.replace("_CLONED", "")
                    clone_needed.append((id, child_name))
                if id not in active_id:
                    plugin_needed.add(id)
            if id not in active_id:
                plugin_needed.add(id)
        
        # Activate necessary plugins.
        for card_type_id in plugin_needed:
            try:
                for plugin in plugins():
                    if plugin.provides == "card_type" and \
                       plugin.id == card_type_id:
                        plugin.activate()
                        break
                else:
                    self._connection.close()
                    self._connection = None
                    self.load_failed = True
                    raise MissingPluginError(info=card_type_id)
            except MissingPluginError:
                raise MissingPluginError(info=card_type_id)
            except:
                self._connection.close()
                self._connection = None
                self.load_failed = True
                raise PluginError(stack_trace=True)
            
        # Create necessary clones.
        for parent_type_id, clone_name in clone_needed:
            parent_instance = card_type_by_id(parent_type_id)
            parent_instance.clone(clone_name)
        
        config()["path"] = contract_path(path, config().basedir)
        log().loaded_database()
        for f in component_manager.get_all("function_hook", "after_load"):
            f.run()

    def save(self, path=None):
        # Don't erase a database which failed to load.
        if self.load_failed == True:
            return -1
        # Update format.
        self.con.execute("""update global_variables set value=? where
            key=?""", (self.version, "version" ))
        # Save database and copy it to different location if needed.
        self.con.commit()
        if not path:
            return
        dest_path = expand_path(path, config().basedir)
        if dest_path != self._path:
            shutil.copy(self._path, dest_path)
            self._path = dest_path
        config()["path"] = contract_path(path, config().basedir)

    def backup(self):
        # TODO: wait for XML export format.
        pass

    def unload(self):
        if self._connection:
            self._connection.commit()
            self._connection.close()
            self._connection = None
            self.load_failed = False
        
    def is_loaded(self):
        return bool(self._connection)

    # Start date.

    def set_start_date(self, start_date_obj):
        self.start_date = start_date_obj
        self.con.execute("insert into global_variables(key,value) values(?,?)",
                        ("start_date", datetime.strftime(self.start_date.start,
                         "%Y-%m-%d %H:%M:%S")))

    def days_since_start(self):
        return self.start_date.days_since_start()

    # Adding, modifying and deleting categories, facts and cards. Commiting is
    # done by calling save in the main controller, in order to have a better
    # control over transaction granularity.

    def add_category(self, category):
        self.con.execute("""insert into categories(name, id, needs_sync)
            values(?,?,?)""", (category.name, category.id, category.needs_sync))
        
    def delete_category(self, category):
        self.con.execute("delete from categories where id=?",
            (category.id, ))
        del category
        
    def update_category(self, category):
        self.con.execute("""update categories set name=?, needs_sync=?
            where id=?""", (category.name, category.needs_sync, category.id))
        
    def get_or_create_category_with_name(self, name):
        sql_res = self.con.execute("""select *
            from categories where name=?""", (name, )).fetchone()
        if sql_res:
            return Category(sql_res["name"], sql_res["id"])
        category = Category(name)
        self.add_category(category)
        return category
    
    def remove_category_if_unused(self, category):
        if self.con.execute("""select count() from categories as cat,
            categories_for_card as cat_c where cat_c._category_id=cat._id and
            cat.id=?""", (category.id, )).fetchone()[0] == 0:
            self.delete_category(category)
    
    def add_fact(self, fact):
        self.load_failed = False
        # Add fact to facts and data_for_fact tables.
        _fact_id = self.con.execute("""insert into facts(id, card_type_id,
            creation_date, modification_date) values(?,?,?,?)""",
            (fact.id, fact.card_type.id, fact.creation_date,
             fact.modification_date)).lastrowid
        # Create data_for_fact.        
        self.con.executemany("""insert into data_for_fact(_fact_id, key, value)
            values(?,?,?)""", ((_fact_id, key, value)
                for key, value in fact.data.items()))

    def update_fact(self, fact):
        # Update fact.
        _fact_id = self.con.execute("select _id from facts where id=?",
            (fact.id, )).fetchone()[0]
        self.con.execute("""update facts set id=?, card_type_id=?,
            creation_date=?, modification_date=? where _id=?""",
            (fact.id, fact.card_type.id, fact.creation_date,
             fact.modification_date, _fact_id))
        # Delete data_for_fact and recreate it.
        self.con.execute("delete from data_for_fact where _fact_id=?",
                (_fact_id, ))
        self.con.executemany("""insert into data_for_fact(_fact_id, key, value)
            values(?,?,?)""", ((_fact_id, key, value)
                for key, value in fact.data.items()))

    def add_card(self, card):
        self.load_failed = False
        _fact_id = self.con.execute("select _id from facts where id=?",
            (card.fact.id, )).fetchone()[0]
        _card_id = self.con.execute("""insert into cards(id, _fact_id,
            fact_view_id, grade, easiness, acq_reps, ret_reps, lapses,
            acq_reps_since_lapse, ret_reps_since_lapse, last_rep, next_rep,
            unseen, extra_data, seen_in_this_session, needs_sync, active,
            in_view) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (card.id, _fact_id, card.fact_view.id, card.grade, card.easiness,
            card.acq_reps, card.ret_reps, card.lapses,
            card.acq_reps_since_lapse, card.ret_reps_since_lapse,
            card.last_rep, card.next_rep, card.unseen, card.extra_data,
            card.seen_in_this_session, card.needs_sync, card.active,
            card.in_view)).lastrowid
        # Link card to its categories.
        # The categories themselves have already been created by
        # default_main_controller calling get_or_create_category_with_name.
        for cat in card.categories:
            _category_id = self.con.execute("""select _id from categories
                where id=?""", (cat.id, )).fetchone()[0]
            self.con.execute("""insert into categories_for_card(_category_id,
                _card_id) values(?,?)""", (_category_id, _card_id))
        log().new_card(card)

    def update_card(self, card):
        _fact_id = self.con.execute("select _id from facts where id=?",
            (card.fact.id, )).fetchone()[0]
        _card_id = self.con.execute("select _id from cards where id=?",
            (card.id, )).fetchone()[0]
        self.con.execute("""update cards set _fact_id=?, fact_view_id=?,
            grade=?, easiness=?, acq_reps=?, ret_reps=?, lapses=?,
            acq_reps_since_lapse=?, ret_reps_since_lapse=?, last_rep=?,
            next_rep=?, unseen=?, extra_data=?, seen_in_this_session=?,
            needs_sync=?, active=?, in_view=? where _id=?""",
            (_fact_id, card.fact_view.id, card.grade, card.easiness,
            card.acq_reps, card.ret_reps, card.lapses,
            card.acq_reps_since_lapse, card.ret_reps_since_lapse,
            card.last_rep, card.next_rep, card.unseen, card.extra_data,
            card.seen_in_this_session, card.needs_sync, card.active,
            card.in_view, _card_id))
        # Link card to its categories.
        # The categories themselves have already been created by
        # default_main_controller calling get_or_create_category_with_name.
        self.con.execute("delete from categories_for_card where _card_id=?",
                         (_card_id, ))
        for cat in card.categories:
            _category_id = self.con.execute("""select _id from categories
                where id=?""", (cat.id, )).fetchone()[0]
            self.con.execute("""insert into categories_for_card(_category_id,
                _card_id) values(?,?)""", (_category_id, _card_id))            

    def delete_fact_and_related_data(self, fact):
        for card in self.cards_from_fact(fact):
            self.delete_card(card)
        _fact_id = self.con.execute("select _id from facts where id=?",
            (fact.id, )).fetchone()[0]
        self.con.execute("delete from facts where _id=?", (_fact_id, ))
        self.con.execute("delete from data_for_fact where _fact_id=?",
                         (_fact_id, ))
        current_card = ui_controller_review().card
        if current_card and current_card.fact == fact:
            scheduler().rebuild_queue()
        del fact
        
    def delete_card(self, card):
        _card_id = self.con.execute("select _id from cards where id=?",
            (card.id, )).fetchone()[0]
        self.con.execute("delete from cards where _id=?", (_card_id, ))
        self.con.execute("delete from categories_for_card where _card_id=?",
                         (_card_id, ))
        for cat in card.categories:
            self.remove_category_if_unused(cat)
        if ui_controller_review().card == card:
            scheduler().rebuild_queue()        
        log().deleted_card(card)
        del card
        
    # Retrieve categories, facts and cards.

    def get_category(self, id):
        sql_res = self.con.execute("""select *
            from categories where id=?""", (id, )).fetchone()
        return Category(sql_res["name"], sql_res["id"])
        
    def _get_fact(self, _id):        
        sql_res = self.con.execute("select * from facts where _id=?",
                                   (_id, )).fetchone()
        if not sql_res:
            raise RuntimeError("Fact _id=%d not found in the database." % _id) 
        # Create dictionary with fact.data.
        data = dict([(cursor["key"], cursor["value"]) for cursor in
            self.con.execute("select * from data_for_fact where _fact_id=?",
            (_id, ))])
        # Create fact.
        fact = Fact(data, card_type_by_id(sql_res["card_type_id"]),
                    id=sql_res["id"],
                    creation_date=sql_res["creation_date"])
        fact.modification_date = sql_res["modification_date"]
        fact.needs_sync = sql_res["needs_sync"]
        return fact

    def get_fact(self, id):
        _fact_id = self.con.execute("select _id from facts where id=?",
                                   (id, )).fetchone()[0]
        return self.get_fact(_fact_id)
    
    def _get_card(self, sql_res):
        fact = self._get_fact(sql_res["_fact_id"])
        for view in fact.card_type.fact_views:
            if view.id == sql_res["fact_view_id"]:
                card = Card(fact, view)
                break
        for attr in ("id", "grade", "easiness", "acq_reps", "ret_reps",
            "lapses", "acq_reps_since_lapse", "ret_reps_since_lapse",
            "last_rep", "next_rep", "unseen", "extra_data",
            "seen_in_this_session", "needs_sync", "active", "in_view"):
            setattr(card, attr, sql_res[attr])
        card.categories = [Category(cursor["name"], cursor["id"]) for cursor in
            self.con.execute("""select cat.name, cat.id from categories as cat,
            categories_for_card as cat_c where cat_c._category_id=cat._id and
            cat_c._card_id=?""", (sql_res["_id"], ))]        
        return card

    def get_card(self, id):
        sql_res = self.con.execute("select * from cards where id=?",
            (id, )).fetchone()
        return self._get_card(sql_res)

    # Activate cards.
    
    def set_cards_active(self, card_types_fact_views, categories):
        return self._turn_on_cards("active", card_types_fact_views,
                                   categories)
    
    def set_cards_in_view(self, card_types_fact_views, categories):
        return self._turn_on_cards("in_view", card_types_fact_views,
                                   categories)
    
    def _turn_on_cards(self, attr, card_types_fact_views, categories):
        # Turn off everything.
        self.con.execute("update cards set active=0")
        # Turn on as soon as there is one active category.
        command = """update cards set %s=1 where _id in (select cards._id
            from cards, categories, categories_for_card where
            categories_for_card._card_id=cards._id and
            categories_for_card._category_id=categories._id and """ % attr
        args = []
        for cat in categories:
            command += "categories.id=? or "
            args.append(cat.id)
        command = command.rsplit("or ", 1)[0] + ")"
        self.con.execute(command, args)
        # Turn off inactive card types and views.
        command = """update cards set %s=0 where _id in (select cards._id
            from cards, facts where cards._fact_id=facts._id and """ % attr
        args = []        
        for card_type, fact_view in card_types_fact_views:
            command += "not (cards.fact_view_id=? and facts.card_type_id=?)"
            command += " and "
            args.append(fact_view.id)  
            args.append(card_type.id)          
        command = command.rsplit("and ", 1)[0] + ")"
        self.con.execute(command, args)

    # Queries.

    def category_names(self):
        return list(cursor[0] for cursor in
            self.con.execute("select name from categories"))

    def cards_from_fact(self, fact):
        _fact_id = self.con.execute("select _id from facts where id=?",
            (fact.id, )).fetchone()[0]
        return list(self._get_card(cursor) for cursor in
            self.con.execute("select * from cards where _fact_id=?",
                             (_fact_id, )))

    def has_fact_with_data(self, fact_data, card_type):
        fact_ids = set()
        for key, value in fact_data.items():
            # If key and value from fact_data are not in the database,
            # we don't have such a fact.
            if not self.con.execute("""select count() from data_for_fact, facts
                where data_for_fact.key=? and data_for_fact.value=? and
                facts._id=data_for_fact._fact_id and facts.card_type_id=?""",
                (key, value, card_type.id)).fetchone()[0]:
                return False
            # If they are present, then we still need to check that they
            # belong to the same fact.
            item_fact_ids = set((cursor["_fact_id"] for cursor in
                self.con.execute("""select _fact_id from data_for_fact, facts
                where data_for_fact.key=? and data_for_fact.value=? and
                facts._id=data_for_fact._fact_id and facts.card_type_id=?""",
                (key, value, card_type.id))))            
            if not fact_ids:
                fact_ids = item_fact_ids
            else:
                fact_ids = fact_ids.intersection(item_fact_ids)
            if not fact_ids:
                return False
        return True

    def duplicates_for_fact(self, fact):
        duplicates = []
        sql_res = self.con.execute("select _id from facts where id=?",
            (fact.id, )).fetchone()
        if not sql_res:
            return duplicates
        _fact_id = sql_res[0]
        for cursor in self.con.execute("""select _id from facts
            where card_type_id=? and not _id=?""",
            (fact.card_type.id, _fact_id)):
            data = dict([(cursor2["key"], cursor2["value"]) for cursor2 in \
                self.con.execute("""select * from data_for_fact where
                _fact_id=?""", (cursor[0], ))])
            for field in fact.card_type.unique_fields:
                if data[field] == fact[field]:
                    duplicates.append(self._get_fact(cursor[0]))
                    break
        return duplicates

    def card_types_in_use(self):
        return [card_type_by_id(cursor[0]) for cursor in self.con.execute\
            ("select distinct card_type_id from facts")]

    def fact_count(self):
        return self.con.execute("select count() from facts").fetchone()[0]

    def card_count(self):
        return self.con.execute("""select count() from cards""").fetchone()[0]

    def non_memorised_count(self):
        return self.con.execute("""select count() from cards
            where active=1 and grade<2""").fetchone()[0]

    def scheduled_count(self, days=0):
        
        """Get number of cards scheduled within 'days' days."""

        count = self.con.execute("""select count() from cards
            where active=1 and grade>=2 and ? >= next_rep - ?""",
            (self.days_since_start(), days)).fetchone()[0]
        return count

    def active_count(self):
        return self.con.execute("""select count() from cards
            where active=1""").fetchone()[0]

    def average_easiness(self):
        average = self.con.execute("""select sum(easiness)/count()
            from cards where active=1""").fetchone()[0]
        if average:
            return average
        else:
            return 2.5

    def _parse_sort_key(self, sort_key):
        if sort_key == "":
            return "_id"
        if sort_key == "random":
            return "random()"
        if sort_key == "interval":
            return "next_rep - last_rep"
        return sort_key

    def cards_due_for_ret_rep(self, sort_key="", limit=-1):
        sort_key = self._parse_sort_key(sort_key)
        return (self._get_card(cursor) for cursor in self.con.execute( \
            """select * from cards where active=1 and grade>=2 and
            ? >= next_rep order by %s limit ?""" % sort_key,
            (self.start_date.days_since_start(), limit )))

    def cards_due_for_final_review(self, grade, sort_key="", limit=-1):
        sort_key = self._parse_sort_key(sort_key)
        return (self._get_card(cursor) for cursor in self.con.execute( \
            """select * from cards where grade=? and lapses>0
            order by %s limit ?""" % sort_key, (grade, limit )))

    def cards_new_memorising(self, grade, sort_key="", limit=-1):
        sort_key = self._parse_sort_key(sort_key)
        return (self._get_card(cursor) for cursor in self.con.execute( \
            """select * from cards where active=1 and grade=? and
            lapses=0 and unseen=0 order by %s limit ?""" % sort_key, (grade, limit )))
    
    def cards_unseen(self, sort_key="", limit=-1):
        sort_key = self._parse_sort_key(sort_key)      
        return (self._get_card(cursor) for cursor in self.con.execute( \
            """select * from cards where active=1 and unseen=1
            order by %s limit ?""" % sort_key, (limit,)))
    
    def cards_learn_ahead(self, sort_key="", limit=-1):
        sort_key = self._parse_sort_key(sort_key)
        return (self._get_card(cursor) for cursor in self.con.execute( \
            """select * from cards where active=1 and grade>=2 and
            ? < next_rep order by %s limit ?""" % sort_key,
            (self.start_date.days_since_start(), limit)))