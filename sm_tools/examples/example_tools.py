from sm_tools.tools import SMValidator
import numpy as np


if __name__ == "__main__":
    print("Example of triple collocation validation: ")
    SMValidator.triple_collocation(np.array([0.15, 0.12]), np.array([0.22, 0.19]), np.array([0.08, 0.1]))
