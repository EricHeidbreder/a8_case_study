import lkml

from lkml import (
    Lexer,
    Parser
)

from lkml.tree import (
    BlockNode,
    PairNode,
    SyntaxToken
)

from dataclasses import replace
from lkml.visitors import BasicTransformer
from funcs import (
    load_with_comments,
    generate_new_filename
)

import os

class AddLabel(BasicTransformer):
        def __init__(self, field_search):
            # Create a properly formatted list from messy user input
            self.field_search = field_search.replace(' ', '').split(',')

        def visit_block(self, node: BlockNode) -> BlockNode:
            # We want to know if any of the search terms are present       
            if any(search_term.lower() in node.name.value for search_term in self.field_search):
                # Generate the new label to add
                new_label = PairNode(
                    SyntaxToken(value='group_label', prefix='', suffix=''),
                    SyntaxToken(value=label_name, prefix='', suffix='\n    ')
                )

                # Not actually the new items yet, creating a list of the orig items
                new_items = list(node.container.items)

                # Now we insert the group label at the front
                new_items.insert(0, new_label)

                # Replacing the original node's items with the new items
                new_container = replace(node.container, items=tuple(new_items))
                new_node = replace(node, container=new_container)

                # rebuild the tree with the new node and continue
                return new_node

            else:
                try:
                    return self._visit_container(node)
                except:
                    return node

print('''

######################################################################
Your project folder is the folder that contains your view folder, model
folder, and all your .lkml files
#######################################################################

''')

# Get the folder path from the user
lookml_base = os.path.normcase(input('Paste your project folder path and press Enter: '))
stop_trigger = ''

# Main loop, user can continue searching through with new terms/labels if they'd like
while stop_trigger.lower() != 'no':
    field_search = input('What search terms are you looking for? Please separate multiple values with commas: ')
    label_name=input('What would you like the new label name to be? ')

    for folder in os.listdir(lookml_base):

        # First, let's only keep folders that don't begin with periods and make sure we're not running any stray .lkml files through this
        if folder[0] != '.' and folder.split('.')[-1] not in ['lkml']:

            for filename in os.listdir(os.path.join(lookml_base, folder)):
                print(filename)

                # ignore any files beginning with a period, and any python or jupyter notebooks files (py or ipynb)
                if filename[0] != '.' and filename.split('.')[-1] not in ['py', 'ipynb']:
                    
                    # Building the tree
                    lookml_path = os.path.join(lookml_base, folder, filename)
                    with open(lookml_path, 'r+') as orig_file:
                        text = orig_file.read()
                    tree = load_with_comments(text)

                    # Add new labels
                    new_tree = tree.accept(AddLabel(field_search=field_search))

                    # Create new file
                    new_filename = generate_new_filename(lookml_path, '_label_added')
                    new_path = os.path.join(lookml_base, folder, new_filename)
                    with open(new_path, 'w+') as new_file:
                        new_file.write(str(new_tree))

    # Done with this task, now we'll see if the user wants to keep going
    stop_trigger = input('''Would you like to keep going? Type "no" and press enter no
    to stop the script.

    Enter your response: ''')
                    


