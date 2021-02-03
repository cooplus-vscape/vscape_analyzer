#!/bin/sh
python build_collection1.py
python build_collection2.py
python build_collection3.py
python delete_repeated_fast.py


# 计时部分
python add_childs.py
python build_whitelist.py
python step1_vcallsite_filter.py
python delete_other_oob.py
python step2_vcallsite_filter.py
python step3_.py
python step4_.py
python step5_.py
python step6_.py
python step7_.py
python step8_.py
python step9_.py
# 计时部分




python step10_.py
