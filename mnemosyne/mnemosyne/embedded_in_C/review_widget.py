#
# review_widget.py <Peter.Bienstman@UGent.be>
#

from mnemosyne.libmnemosyne.ui_components.review_widget import ReviewWidget \
     as GenericReviewWidget


class ReviewWidget(GenericReviewWidget):

    # TMP

    def callback(self, *args):
        pass

    def read_from_socket(self):
        pass

    def set_question_label(self, text):
        self.callback(text)
        
    def set_question(self, text):
        self.callback(text)

    def clear_question(self):
        self.callback()
        
    def set_question_box_visible(self, visible):
        self.callback(visible)

    def set_answer(self, text):
        self.callback(text)
        
    def clear_answer(self):
        self.callback()
            
    def set_answer_box_visible(self, visible):
        self.callback(visible)

    def update_show_button(self, text, default, enabled):
        self.callback(text, default, enabled)

    def set_grades_enabled(self, enabled):
        self.callback(enabled)
        
    def set_grade_enabled(self, grade, is_enabled):
        self.callback(grade, is_enabled)
        
    def set_default_grade(self, grade):
        self.callback(grade)
        
    def show_answer(self):
        self.callback()        
           
    def grade_answer(self, grade):
        self.callback(grade)

    def set_grades_title(self, text): 
        self.callback(text)
            
    def set_grade_text(self, grade, text): 
        self.callback(grade, text)
            
    def set_grade_tooltip(self, grade, text): 
        self.callback(grade, text)

    def update_status_bar(self):
        self.callback()




       
