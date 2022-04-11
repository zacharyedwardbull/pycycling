Search.setIndex({docnames:["index","pycycling","pycycling.battery_service","pycycling.cycling_power_service","pycycling.cycling_speed_cadence_service","pycycling.heart_rate_service","pycycling.sterzo","pycycling.tacx_trainer_control"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":5,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.todo":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["index.rst","pycycling.rst","pycycling.battery_service.rst","pycycling.cycling_power_service.rst","pycycling.cycling_speed_cadence_service.rst","pycycling.heart_rate_service.rst","pycycling.sterzo.rst","pycycling.tacx_trainer_control.rst"],objects:{"":[[1,0,0,"-","pycycling"]],"pycycling.battery_service":[[2,1,1,"","BatteryService"]],"pycycling.battery_service.BatteryService":[[2,2,1,"","get_battery_level"]],"pycycling.cycling_power_service":[[3,1,1,"","CyclingPowerFeature"],[3,1,1,"","CyclingPowerMeasurement"],[3,1,1,"","CyclingPowerService"],[3,1,1,"","CyclingPowerVector"],[3,1,1,"","DistributeSystemSupport"],[3,1,1,"","InstantaneousMeasurementDirection"],[3,1,1,"","SensorLocation"],[3,1,1,"","SensorMeasurementContext"]],"pycycling.cycling_power_service.CyclingPowerFeature":[[3,3,1,"","accumulated_energy_supported"],[3,3,1,"","accumulated_torque_supported"],[3,3,1,"","chain_length_adjustment_supported"],[3,3,1,"","chain_weight_adjustment_supported"],[3,3,1,"","crank_length_adjustment_supported"],[3,3,1,"","crank_rev_supported"],[3,3,1,"","cycling_power_measurement_content_masking_supported"],[3,3,1,"","dead_spot_angles_supported"],[3,3,1,"","distribute_system_support"],[3,3,1,"","enhanced_offset_compensation_supported"],[3,3,1,"","extreme_magnitudes_supported"],[3,3,1,"","factory_calibration_date_supported"],[3,3,1,"","instantaneous_measurement_direction_supported"],[3,3,1,"","multiple_locations_supported"],[3,3,1,"","offset_compensation_supported"],[3,3,1,"","pedal_power_balance_supported"],[3,3,1,"","sensor_measurement_context"],[3,3,1,"","span_length_adjustment_supported"],[3,3,1,"","wheel_rev_supported"]],"pycycling.cycling_power_service.CyclingPowerMeasurement":[[3,3,1,"","accumulated_energy"],[3,3,1,"","accumulated_torque"],[3,3,1,"","bottom_dead_spot_angle"],[3,3,1,"","cumulative_crank_revs"],[3,3,1,"","cumulative_wheel_revs"],[3,3,1,"","instantaneous_power"],[3,3,1,"","last_crank_event_time"],[3,3,1,"","last_wheel_event_time"],[3,3,1,"","maximum_force_magnitude"],[3,3,1,"","maximum_torque_magnitude"],[3,3,1,"","minimum_force_magnitude"],[3,3,1,"","minimum_torque_magnitude"],[3,3,1,"","pedal_power_balance"],[3,3,1,"","top_dead_spot_angle"]],"pycycling.cycling_power_service.CyclingPowerService":[[3,2,1,"","disable_cycling_power_measurement_notifications"],[3,2,1,"","disable_cycling_power_vector_notifications"],[3,2,1,"","enable_cycling_power_measurement_notifications"],[3,2,1,"","enable_cycling_power_vector_notifications"],[3,2,1,"","get_cycling_power_feature"],[3,2,1,"","get_sensor_location"],[3,2,1,"","set_cycling_power_measurement_handler"],[3,2,1,"","set_cycling_power_vector_handler"]],"pycycling.cycling_power_service.CyclingPowerVector":[[3,3,1,"","cumulative_crank_revs"],[3,3,1,"","first_crank_measurement_angle"],[3,3,1,"","instantaneous_force_magnitudes"],[3,3,1,"","instantaneous_measurement_direction"],[3,3,1,"","instantaneous_torque_magnitudes"],[3,3,1,"","last_crank_event_time"]],"pycycling.cycling_power_service.DistributeSystemSupport":[[3,3,1,"","distributed_system_support"],[3,3,1,"","no_distributed_system_support"],[3,3,1,"","rfu"],[3,3,1,"","unspecified"]],"pycycling.cycling_power_service.InstantaneousMeasurementDirection":[[3,3,1,"","lateral_component"],[3,3,1,"","radial_component"],[3,3,1,"","tangential_component"],[3,3,1,"","unknown"]],"pycycling.cycling_power_service.SensorLocation":[[3,3,1,"","chain_ring"],[3,3,1,"","chainstay"],[3,3,1,"","chest"],[3,3,1,"","front_hub"],[3,3,1,"","front_wheel"],[3,3,1,"","hip"],[3,3,1,"","in_shoe"],[3,3,1,"","left_crank"],[3,3,1,"","left_pedal"],[3,3,1,"","other"],[3,3,1,"","rear_dropout"],[3,3,1,"","rear_hub"],[3,3,1,"","rear_wheel"],[3,3,1,"","right_crank"],[3,3,1,"","right_pedal"],[3,3,1,"","spider"],[3,3,1,"","top_of_shoe"]],"pycycling.cycling_power_service.SensorMeasurementContext":[[3,3,1,"","force_based"],[3,3,1,"","torque_based"]],"pycycling.cycling_speed_cadence_service":[[4,1,1,"","CSCFeature"],[4,1,1,"","CSCMeasurement"],[4,1,1,"","CyclingSpeedCadenceService"]],"pycycling.cycling_speed_cadence_service.CSCFeature":[[4,3,1,"","crank_rev_supported"],[4,3,1,"","multiple_locations_supported"],[4,3,1,"","wheel_rev_supported"]],"pycycling.cycling_speed_cadence_service.CSCMeasurement":[[4,3,1,"","cumulative_crank_revs"],[4,3,1,"","cumulative_wheel_revs"],[4,3,1,"","last_crank_event_time"],[4,3,1,"","last_wheel_event_time"]],"pycycling.cycling_speed_cadence_service.CyclingSpeedCadenceService":[[4,2,1,"","disable_csc_measurement_notifications"],[4,2,1,"","enable_csc_measurement_notifications"],[4,2,1,"","get_csc_feature"],[4,2,1,"","set_csc_measurement_handler"]],"pycycling.heart_rate_service":[[5,1,1,"","HeartRateMeasurement"],[5,1,1,"","HeartRateService"]],"pycycling.heart_rate_service.HeartRateMeasurement":[[5,3,1,"","bpm"],[5,3,1,"","energy_expended"],[5,3,1,"","rr_interval"],[5,3,1,"","sensor_contact"]],"pycycling.heart_rate_service.HeartRateService":[[5,2,1,"","disable_hr_measurement_notifications"],[5,2,1,"","enable_hr_measurement_notifications"],[5,2,1,"","set_hr_measurement_handler"]],"pycycling.sterzo":[[6,1,1,"","Sterzo"]],"pycycling.sterzo.Sterzo":[[6,2,1,"","disable_steering_measurement_notifications"],[6,2,1,"","enable_steering_measurement_notifications"],[6,2,1,"","set_steering_measurement_callback"]],"pycycling.tacx_trainer_control":[[7,1,1,"","CommandStatus"],[7,1,1,"","CommandStatusData"],[7,1,1,"","EquipmentType"],[7,1,1,"","FEState"],[7,1,1,"","GeneralFEData"],[7,1,1,"","RoadSurface"],[7,1,1,"","SpecificTrainerData"],[7,1,1,"","TacxTrainerControl"],[7,1,1,"","TargetPowerLimit"]],"pycycling.tacx_trainer_control.CommandStatus":[[7,3,1,"","fail"],[7,3,1,"","not_supported"],[7,3,1,"","rejected"],[7,3,1,"","success"],[7,3,1,"","uninitialized"]],"pycycling.tacx_trainer_control.CommandStatusData":[[7,3,1,"","command_status"],[7,3,1,"","data"],[7,3,1,"","last_received_command"]],"pycycling.tacx_trainer_control.EquipmentType":[[7,3,1,"","climber"],[7,3,1,"","elliptical"],[7,3,1,"","nordic_skier"],[7,3,1,"","reserved"],[7,3,1,"","rower"],[7,3,1,"","trainer"],[7,3,1,"","treadmill"]],"pycycling.tacx_trainer_control.FEState":[[7,3,1,"","finished"],[7,3,1,"","in_use"],[7,3,1,"","ready"],[7,3,1,"","reserved"]],"pycycling.tacx_trainer_control.GeneralFEData":[[7,3,1,"","distance_travelled"],[7,3,1,"","elapsed_time"],[7,3,1,"","equipment_type"],[7,3,1,"","fe_state"],[7,3,1,"","heart_rate"],[7,3,1,"","lap_toggle"],[7,3,1,"","speed"]],"pycycling.tacx_trainer_control.RoadSurface":[[7,3,1,"","BRICK_ROAD"],[7,3,1,"","CATTLE_GRID"],[7,3,1,"","COBBLESTONES_HARD"],[7,3,1,"","COBBLESTONES_SOFT"],[7,3,1,"","CONCRETE_PLATES"],[7,3,1,"","GRAVEL"],[7,3,1,"","ICE"],[7,3,1,"","OFF_ROAD"],[7,3,1,"","SIMULATION_OFF"],[7,3,1,"","WOODEN_BOARDS"]],"pycycling.tacx_trainer_control.SpecificTrainerData":[[7,3,1,"","accumulated_power"],[7,3,1,"","fe_state"],[7,3,1,"","instantaneous_cadence"],[7,3,1,"","instantaneous_power"],[7,3,1,"","lap_toggle"],[7,3,1,"","power_calibration_required"],[7,3,1,"","resistance_calibration_required"],[7,3,1,"","target_power_limits"],[7,3,1,"","trainer_status"],[7,3,1,"","update_event_count"],[7,3,1,"","user_configuration_required"]],"pycycling.tacx_trainer_control.TacxTrainerControl":[[7,2,1,"","disable_fec_notifications"],[7,2,1,"","enable_fec_notifications"],[7,2,1,"","request_data_page"],[7,2,1,"","set_basic_resistance"],[7,2,1,"","set_command_status_data_page_handler"],[7,2,1,"","set_general_fe_data_page_handler"],[7,2,1,"","set_neo_modes"],[7,2,1,"","set_specific_trainer_data_page_handler"],[7,2,1,"","set_target_power"],[7,2,1,"","set_track_resistance"],[7,2,1,"","set_user_configuration"],[7,2,1,"","set_wind_resistance"]],"pycycling.tacx_trainer_control.TargetPowerLimit":[[7,3,1,"","limit_reached"],[7,3,1,"","operating_at_target_or_no_target_set"],[7,3,1,"","user_speed_too_high"],[7,3,1,"","user_speed_too_low"]],pycycling:[[2,0,0,"-","battery_service"],[3,0,0,"-","cycling_power_service"],[4,0,0,"-","cycling_speed_cadence_service"],[5,0,0,"-","heart_rate_service"],[6,0,0,"-","sterzo"],[7,0,0,"-","tacx_trainer_control"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute"},terms:{"0":[2,3,4,5,7],"1":[1,2,3,4,5,7],"10":[3,7],"100":[2,7],"11":3,"12":3,"13":3,"14":3,"15":3,"16":3,"17":3,"18":3,"2":[3,4,5,7],"20":7,"255":7,"3":[3,4,5,7],"30":3,"4":[3,7],"40":7,"4d77":[3,7],"5":[3,7],"50":7,"6":[3,7],"6760":[3,7],"7":[3,7],"8":[3,7],"8ddac1cc9a":[3,7],"9":[3,7],"961e":[3,7],"case":7,"class":[1,2,3,4,5,6,7],"enum":[3,7],"import":[1,2,3,7],"int":2,"return":2,"try":7,"while":[2,7],A:[2,3,7],For:7,In:7,It:7,The:[1,7],These:7,To:7,__main__:[1,2,3,7],__name__:[1,2,3,7],acceler:7,accumulated_energi:3,accumulated_energy_support:3,accumulated_pow:7,accumulated_torqu:3,accumulated_torque_support:3,act:7,activ:7,ad:2,address:[0,2,3,7],adjust:7,against:7,air:7,alia:[3,4,5,7],all:1,allow:7,along:7,also:[2,3,7],alter:7,an:[1,2,3,7],ani:7,ant:7,appli:7,applic:7,ar:7,area:7,around:[1,2],assum:7,async:[1,2,3,4,5,6,7],asyncio:[1,2,3,7],avail:1,await:[1,2,3,7],back:7,backend:2,base:[2,3,4,5,6,7],basebleakcli:2,basic:7,batteri:2,battery_level:2,battery_servic:[0,1],batteryservic:2,becaus:7,befor:7,behind:7,between:7,bicycl:7,bicycle_weight:7,bicycle_wheel_diamet:7,bike:7,ble:7,bleak:[1,2,3,7],bleakclient:[2,3,7],bluetooth:[1,2,3,7],both:7,bottom_dead_spot_angl:3,bpm:5,brake:7,brick_road:7,bring:7,broadcast:3,c:7,cadenc:7,callback:[3,4,5,6,7],can:[1,7],cattle_grid:7,chain:7,chain_length_adjustment_support:3,chain_r:3,chain_weight_adjustment_support:3,chainstai:3,chang:7,charg:2,chest:3,client:[1,2,3,4,5,6,7],climber:7,coast:7,cobblestones_hard:7,cobblestones_soft:7,code:1,coeffici:7,coefficient_of_rolling_resist:7,cog:7,come:7,command_statu:7,commandstatu:7,commandstatusdata:7,common:7,comput:7,concrete_pl:7,configur:7,consol:[2,3,7],constant:7,correct:7,counter:7,crank_length_adjustment_support:3,crank_rev_support:[3,4],cross:1,cscfeatur:4,cscmeasur:4,cumulative_crank_rev:[3,4],cumulative_wheel_rev:[3,4],current:2,cycl:[1,3,7],cycling_power_measurement_content_masking_support:3,cycling_power_servic:[0,1],cycling_speed_cadence_servic:[0,1],cyclingpowerfeatur:3,cyclingpowermeasur:3,cyclingpowerservic:3,cyclingpowervector:3,cyclingspeedcadenceservic:4,cyclist:7,d:1,damag:7,data:[3,7],dead_spot_angles_support:3,def:[1,2,3,7],defin:7,demonstr:[1,7],densiti:7,detail:7,devic:[0,2,3,7],device_address:[1,2,3,7],diamet:7,differ:7,dimensionless:7,directli:7,disable_csc_measurement_notif:4,disable_cycling_power_measurement_notif:3,disable_cycling_power_vector_notif:3,disable_fec_notif:7,disable_hr_measurement_notif:5,disable_steering_measurement_notif:6,discharg:2,discov:1,distance_travel:7,distribute_system_support:3,distributed_system_support:3,distributesystemsupport:3,document:1,doe:7,down:7,draft:7,drafting_factor:7,drag:7,dynam:7,eaaa3d1f:[3,7],each:[1,7],elapsed_tim:7,electromagnet:7,ellipt:7,enabl:7,enable_csc_measurement_notif:4,enable_cycling_power_measurement_notif:3,enable_cycling_power_vector_notif:3,enable_fec_notif:7,enable_hr_measurement_notif:5,enable_steering_measurement_notif:6,energy_expend:5,enhanced_offset_compensation_support:3,enumer:[3,7],environ:[1,2,3,7],equat:7,equipment_typ:7,equipmenttyp:7,erg:7,etc:7,even:7,exampl:[0,1],exert:7,explain:7,extreme_magnitudes_support:3,f:2,facilit:7,factory_calibration_date_support:3,fail:7,fairli:7,fals:7,favour:7,fe:7,fe_stat:7,featur:7,feel:7,festat:7,few:7,field:[3,4,5,7],finalis:7,finish:7,first:7,first_crank_measurement_angl:3,flywheel:7,follow:1,forc:7,force_bas:3,from:[1,2,3,7],front:7,front_hub:3,front_wheel:3,frontal:7,ftm:7,full:7,fulli:2,fundament:7,gear:7,gear_ratio:7,generalfedata:7,get:7,get_battery_level:2,get_csc_featur:4,get_cycling_power_featur:3,get_event_loop:[1,2,3,7],get_sensor_loc:3,go:7,grade:7,gravel:7,gravit:7,h:7,ha:[1,7],hard:7,hardcod:1,harder:7,head:7,heart_rat:7,heart_rate_servic:[0,1],heartratemeasur:5,heartrateservic:5,heavi:7,heavier:7,help:7,here:[2,7],hip:3,howev:7,i:7,ic:7,id:1,in_sho:3,in_us:7,inclin:7,includ:1,incorrect:7,index:0,indic:2,inerti:7,info:7,inform:[2,3,7],initi:7,instantaneous_cad:7,instantaneous_force_magnitud:3,instantaneous_measurement_direct:3,instantaneous_measurement_direction_support:3,instantaneous_pow:[3,7],instantaneous_torque_magnitud:3,instantaneousmeasurementdirect:3,instead:7,intens:7,interact:[1,2,3,7],intern:7,is_connect:[3,7],isokinet:7,isokinetic_mod:7,isokinetic_spe:7,isoton:7,kg:7,kilogram:7,km:7,lap_toggl:7,last_crank_event_tim:[3,4],last_received_command:7,last_wheel_event_tim:[3,4],later:7,lateral_compon:3,law:7,left_crank:3,left_ped:3,level:2,limit_reach:7,list:1,littl:7,ll:7,loop:[1,2,3,7],m:7,mai:7,maintain:7,make:7,mani:7,mass:7,maximum_force_magnitud:3,maximum_torque_magnitud:3,mean:7,measur:3,meter:3,method:2,metr:7,minimum_force_magnitud:3,minimum_torque_magnitud:3,mode:[0,1],modul:0,most:[3,7],multiple_locations_support:[3,4],my_measurement_handl:3,my_page_handl:7,need:1,neg:7,neo:7,newton:7,no_distributed_system_support:3,nordic_ski:7,not_support:7,note:7,now:7,number:[1,3,4,5,7],object:[1,2,3,4,5,6,7],obtain:[0,2,3,7],off_road:7,offset_compensation_support:3,onli:7,oper:[0,1],operating_at_target_or_no_target_set:7,oppon:7,order:7,os:[1,2,3,7],other:[1,3,7],output:7,packag:0,page:0,page_numb:7,paramet:[2,7],pedal:7,pedal_power_bal:3,pedal_power_balance_support:3,percentag:2,peripher:1,physic:7,plai:7,platform:1,pleas:[2,3,7],posit:7,power:[3,7],power_calibration_requir:7,preset:7,print:[1,2,3,7],product:7,protocol:7,provid:1,python:1,pythonasynciodebug:[1,2,3,7],radial_compon:3,rather:7,ratio:7,readi:7,rear:7,rear_dropout:3,rear_hub:3,rear_wheel:3,recommend:7,refer:7,reject:7,releas:7,replac:1,repres:[2,7],request_data_pag:7,requir:7,reserv:7,resist:7,resistance_calibration_requir:7,rfu:3,rider:7,right_crank:3,right_ped:3,ring:7,road:7,road_surface_pattern:7,road_surface_pattern_intens:7,roadsurfac:7,roll:7,rower:7,rr_interv:5,run:[1,2,3,7],run_until_complet:[1,2,3,7],s:7,scale:7,script:1,search:0,second:7,see:[2,3,7],sensor_contact:5,sensor_measurement_context:3,sensorloc:3,sensormeasurementcontext:3,servic:[2,3],set:7,set_basic_resist:7,set_command_status_data_page_handl:7,set_csc_measurement_handl:4,set_cycling_power_measurement_handl:3,set_cycling_power_vector_handl:3,set_general_fe_data_page_handl:7,set_hr_measurement_handl:5,set_neo_mod:7,set_specific_trainer_data_page_handl:7,set_steering_measurement_callback:6,set_target_pow:7,set_track_resist:7,set_user_configur:7,set_wind_resist:7,simpl:7,simul:7,simulation_off:7,sleep:[3,7],slope:7,slow:7,small:7,smart:[0,1],snippet:1,so:7,some:3,somewhat:7,sourc:[2,3,4,5,6,7],span_length_adjustment_support:3,special:7,specif:[2,7],specifi:7,specifictrainerdata:7,speed:7,spider:3,standard:7,sterzo:[0,1],stop:7,str:[1,2,3,7],strongli:7,submodul:0,success:7,support:[2,3,7],surfac:7,tacx:7,tacx_trainer_control:[0,1],tacxtrainercontrol:7,tail:7,tangential_compon:3,target:7,target_pow:7,target_power_limit:7,targetpowerlimit:7,teeth:7,than:7,thei:7,theori:7,therefor:7,thi:[1,2,3,7],think:7,through:7,top_dead_spot_angl:3,top_of_sho:3,torque_bas:3,track:7,train:7,trainer:[0,1,3],trainer_statu:7,treadmil:7,tupl:[3,4,5,7],turbo:[3,7],two:7,type:7,typic:7,understand:7,uniniti:7,uniqu:7,unit:7,unknown:3,unspecifi:3,untest:7,update_event_count:7,us:[1,7],usag:1,user:7,user_configuration_requir:7,user_speed_too_high:7,user_speed_too_low:7,user_weight:7,util:2,valid:2,valu:[2,3,7],variat:7,variou:1,veloc:7,virtual:7,wa:7,watt:7,weight:7,what:7,wheel:7,wheel_rev_support:[3,4],when:7,where:7,which:[1,2,3,7],wind:7,wind_resistance_coeffici:7,wind_spe:7,wooden_board:7,word:7,work:7,would:7,wrap:1,wrapper:2,you:[1,7],your:[0,2,3,7],zero:7,zwift:7},titles:["Welcome to pycycling\u2019s documentation!","pycycling package","pycycling.battery_service module","pycycling.cycling_power_service module","pycycling.cycling_speed_cadence_service module","pycycling.heart_rate_service module","pycycling.sterzo module","pycycling.tacx_trainer_control module"],titleterms:{address:1,battery_servic:2,content:[0,1],cycling_power_servic:3,cycling_speed_cadence_servic:4,devic:1,document:0,exampl:[2,3,7],heart_rate_servic:5,indic:0,mode:7,modul:[1,2,3,4,5,6,7],obtain:1,oper:7,packag:1,pycycl:[0,1,2,3,4,5,6,7],s:0,smart:7,sterzo:6,submodul:1,tabl:0,tacx_trainer_control:7,trainer:7,welcom:0,your:1}})