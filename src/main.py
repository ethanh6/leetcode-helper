from LeetCodeHelper import *
import sys, json

if __name__ == '__main__':
    LCH = LeetcodeHelper(refresh_data=False)
    # try:
    mode = sys.argv[1]

    # add questions and update my_db.json
    if mode == "add":
        if int(sys.argv[2])+3 != len(sys.argv):
            exit("input not valid: {}".format(sys.argv))
        for i, q in enumerate(sys.argv):
            if int(i) < 3: continue
            LCH.build_question(q_id=int(i))
        LCH.build_working_dir_for_questions()
        LCH.write_to_my_db()

    # read my_db.json and generate README.md
    elif mode == "gen":
        pass

    else:
        exit("Not valid mode")

    # except Exception as e:
        # exit(e)

