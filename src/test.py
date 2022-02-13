from LeetCodeHelper import *

if __name__ == '__main__':
    LCH = LeetcodeHelper(refresh_data=False)
    LCH.build_question(q_id=1)
    print(LCH.get_all_built_question())
    print(LCH.get_single_built_question(q_id=1))
    print(LCH.get_single_built_question(q_id=2))
