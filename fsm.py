from transitions.extensions import GraphMachine


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_hamburger(self, update):
        text = update.message.text
        return text.lower() == 'hamburger'

    def is_going_to_fries(self, update):
        text = update.message.text
        return text.lower() == 'fries'

    def on_enter_hamburger(self, update):
        update.message.reply_text("for here or to go")
#        self.foward(update)

    def on_exit_hamburger(self, update):
        print('Leaving state1')

    def on_enter_fries(self, update):
        update.message.reply_text("for here or to go")
#        self.foward(update)

    def on_exit_fries(self, update):
        print('Leaving state2')

    def is_going_to_for_here(self, update):
        text = update.message.text
        return text.lower() == 'for here'

    def is_going_to_to_go(self, update):
        text = update.message.text
        return text.lower() == 'to go'

    def on_enter_for_here(self, update):
        update.message.reply_text("ok,for here")
        self.go_back(update)

    def on_enter_to_go(self, update):
        update.message.reply_text("ok,to go")
        self.go_back(update)

    def on_exit_for_here(self, update):
        print('Leaving state1')
