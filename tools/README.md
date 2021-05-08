python process_result.py [trajectory_result].csv [data_sequence_name] 

[trajectory_result].csv is the output of VINS-Mono/VINS-RGBD/DUI-VIO, some examples can be found in test_results 
[data_sequence_name] are the names defined in the IROS benchmark paper 

e.g. python process_result.py lab_motion2.csv lab-motion2  

Next, use evo to evaluate the results compared to the ground truth 

e.g. evo_ape tum lab_simple3_gt.csv lab_simple3_tum.csv -a -p
