from LeetCodeHelper import *
import sys, json

if __name__ == '__main__':
    LCH = LeetcodeHelper(refresh_data=False)
    # try:
    mode = sys.argv[1]

    # add questions and update my_db.json
    if mode == "add":
        # check inputs
        if int(sys.argv[2])+3 != len(sys.argv):
            exit("input not valid: {}".format(sys.argv))

        # build questions
        # print("building questions")
        for i, q in enumerate(sys.argv):
            if int(i) < 3:
                continue
            LCH.build_question(q_id=int(q))

        # print("build working dir for questions")
        # build working dirs for these questions
        LCH.build_working_dir_for_questions()

        # write to my_db
        LCH.write_to_my_db()

    # read my_db.json and generate README.md
    elif mode == "gen":
        exit("gen mode not implemented yet")

    else:
        exit("Not valid mode")
