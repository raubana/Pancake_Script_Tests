from ops_arithmatic import *
from ops_relational import *
from ops_equality import *
from ops_logical import *
from ops_assignment import *

OPERATORS = [
				#ARITHMATIC OPS
				Op_Addition,
			 	Op_Subtraction,
				Op_Negate,
			 	Op_Multiplication,
			 	Op_Division,
			 	Op_Modulus,
			 	Op_Power,

				#RELATIONAL OPS
				Op_GreaterThan,
				Op_GreaterThanEqualTo,
				Op_LessThan,
				Op_LessThanEqualTo,

				#EQUALITY OPS
				Op_EqualTo,
				Op_NotEqualTo,

				#LOGICAL OPS
				Op_And,
				Op_Or,
				Op_Not,

				#ASSIGNMENT OPS
				Op_Assign
			 ]