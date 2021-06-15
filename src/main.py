from src.config.nodepair import NodePair
from src.data import initial_connections
from src.ui.ui import SetupRoutesForm, CloseReason, FindRoutesForm

if __name__ == '__main__':
    connections = list(map(lambda city_tuple: NodePair(city_tuple[0], city_tuple[1]), initial_connections))

    setupForm = SetupRoutesForm(connections)
    setupForm.show()

    while setupForm.close_reason == CloseReason.OK:
        findForm = FindRoutesForm(setupForm.list_of_connections)
        findForm.show()

        if findForm.close_reason != CloseReason.EDIT:
            break

        setupForm = SetupRoutesForm(findForm.list_of_connections)
        setupForm.show()

        if setupForm.close_reason == CloseReason.CLOSE:
            setupForm.list_of_connections = findForm.list_of_connections
            setupForm.close_reason = CloseReason.OK
