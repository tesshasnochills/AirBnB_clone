#!/usr/bin python3
"""module - the console"""

import cmd
import models
from models.base_model import BaseModel
from models.city import City
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review


classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
        }
dot_cmd = ['all', 'count', 'show', 'destroy', 'update']


class HBNBCommand(cmd.Cmd):
    """ the command line for the hbnb """

    prompt = '(hbnb) '

    def do_quit(self, line):
        """Quit command to exit the program.\n"""

        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""

        print()
        return True

    def emptyline(self):
        """ the command line should do nothing"""
        pass

    def do_help(self, line):
        """ display help information about the commands"""
        cmd.Cmd.do_help(self, line)

    def do_create(self, args):
        "Usage: create <class>\n        "
        "Create a new class instance and print its id."
        args = args.split()
        if not args:
            print("** class name missing **")
            return
        class_nm = args[0]
        if class_nm not in classes:
            print("** class doesn't exist **")
            return
        new_inst = classes[class_nm]()
        new_inst.save()
        print(new_inst.id)

    def do_show(self, args):
        "Usage: show <class> <id> or <class>.show(<id>)\n        "
        "Display the string representation of a class instance of"
        " a given id."

        args = args.split()
        if not args:
            print("** class name missing **")
            return
        class_nm = args[0]
        if class_nm not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        class_id = args[1]
        all_inst = models.storage.all()
        found = False
        for key, instance in all_inst.items():
            if class_nm in key and class_id in key:
                found = True
                print(instance)
                break
        if not found:
            print("** no instance found **")

    def do_destroy(self, args):
        "Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
        "Delete a class instance of a given id."
        args = args.split()
        if not args:
            print("** class name missing **")
            return
        class_nm = args[0]
        if class_nm not in classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id is missing **")
            return

        found = False
        inst_id = args[1]
        key = "{}.{}".format(class_nm, inst_id)
        all_inst = models.storage.all()
        instance = all_inst.pop(key)
        if instance:
            del (instance)
            models.storage.save()
            found = True
        if not found:
            print("** no instance found **")

    def do_all(self, args):
        "Usage: all or all <class> or <class>.all()\n        "
        "Display string representations of all instances of a given class"
        ".\n        If no class is specified, displays all instantiated "
        "objects."

        args = args.split(" ")
        class_nm = args[0]
        if class_nm:
            if class_nm not in classes:
                print("** class doesn't exist **")
                return
        else:
            all_instances = models.storage.all()
            for key, instances in all_instances.items():
                print([str(instances)])
        if class_nm in classes:
            all_instances = models.storage.all()
            for key, instance in all_instances.items():
                if class_nm in key:
                    print([str(instance)])

    def do_update(self, args):
        "Usage: update <class> <id> <attribute_name> <attribute_value> or"
        "\n  <class>.update(<id>, <attribute_name>, <attribute_value"
        ">) or\n       <class>.update(<id>, <dictionary>)\n        "
        "Update a class instance of a given id by adding or updating\n   "
        "     a given attribute key/value pair or dictionary."
        args = args.split()
        class_nm = args[0]

        if len(args) < 1:
            print("** class name missing **")
            return
        if class_nm not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        inst_id = args[1]
        found = False
        key = "{}.{}".format(class_nm, inst_id)
        all_inst = models.storage.all()
        if len(args) < 3:
            print("** atribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attribute_nm = args[2]
        attribute_vl = args[3]

        for key, instance in all_inst.items():
            if inst_id in key:
                found = True
                if len(args) < 5:
                    setattr(instance,
                            attribute_nm,
                            attribute_vl.strip('"'))
                    models.storage.save()

        if not found:
            print("** no instance found **")
            return

    def precmd(self, args):
        """Reformat command line for advanced command syntax.
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in args and '(' in args and ')' in args):
            return args

        try:  # parse line left to right
            pline = args[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in dot_cmd:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' \
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line
        
    def default(self, line):
        """ class command handler """
        ln = line.split('.', 1)
        if len(ln) < 2:
            print('*** Unknown syntax:', ln[0])
            return False
        class_nm , line = ln[0], ln[1]
        if class_nm not in list(self.classes.keys()):
            print('*** Unknown syntax: {}.{}'.format(class_nm, line))
            return False
        ln = line.split('(', 1)
        if len(ln) < 2:
            print('*** Unknown syntax: {}.{}'.format(class_nm, ln[0]))
            return False
        method_name, args = ln[0], ln[1].rstrip(')')
        if method_name not in ['all', 'count', 'show', 'destroy', 'update']:
            print('*** Unknown syntax: {}.{}'.format(class_nm, line))
            return False
        if method_name == 'all':
            self.do_all(class_nm)
        elif method_name == 'count':
            print(self.count_class(class_nm))
        elif method_name == 'show':
            self.do_show(class_nm + " " + args.strip('"'))
        elif method_name == 'destroy':
            self.do_destroy(class_nm + " " + args.strip('"'))
        elif method_name == 'update':
            curly_l, curly_r = args.find('{'), args.find('}')
            check = None
            if args[curly_l:curly_r + 1] != '':
                check = eval(args[curly_l:curly_r + 1])
            ln = args.split(',', 1)
            obj_id, args = ln[0].strip('"'), ln[1]
            if check and type(check) is dict:
                self.handle_dict(class_nm, obj_id, check)
            else:
                from shlex import shlex
                args = args.replace(',', ' ', 1)
                ln = list(shlex(args))
                ln[0] = ln[0].strip('"')
                self.do_update(" ".join([class_nm, obj_id, ln[0], ln[1]]))

    def do_count(self, args):
        "Usage: count <class> or <class>.count()\n        "
        "Retrieve the number of instances of a given class."
        count = 0
        all_instances = models.storage.all()
        for key, value in all_instances.items():
            if args[0] in key:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
