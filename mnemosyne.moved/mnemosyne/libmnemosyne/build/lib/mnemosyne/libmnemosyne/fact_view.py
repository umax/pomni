#
# fact_view.py <Peter.Bienstman@UGent.be>
#


class FactView(object):

    """Sequence of fields from a fact to form a question and an answer.
    A fact view needs an id as well as a name, because the name can
    change for different translations. 
    
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.q_fields = []
        self.a_fields = []
        self.required_fields = []
        self.a_on_top_of_q = False

    def __eq__(self, other):
        try:
            return self.id == other.id
        except:
            return False      

    