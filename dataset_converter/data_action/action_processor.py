from dataset_converter.data_action.provider import Provider as action_provider


class ActionProcessor(object):
    """docstring for ActionProcessor"""
    def __init__(self, action_list, annotations_container):
        super(ActionProcessor, self).__init__()
        self.action_list = action_list
        self.annotations_container = annotations_container

    def process(self):
        for elem in self.action_list:

            # init class
            action = action_provider.get_action(elem)

            # process
            self.annotations_container = action.process(self.annotations_container)
        return self.annotations_container
