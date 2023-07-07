# DEEPLABCUT analays
What does this code do:
This code is designed to easily check the performance of different parameters for network training.

How to use the code:
To begin with, you need to have a project with labeled data, if there is no such, then you need to create a project and label frames. Then open the file config.json and in labeled_project_path specify the path to your project. After that, specify the desired values in the parameters (the recommendation in maxiters is to set a small value, especially if you have a weak PC. This will avoid eternal loading) and run dlc_analays.py via cmd.

IMPORTANT:                                                                          
Put all the values in the parameters exclusively in the [ ] lists to avoid errors. This is also necessary in order to check different parameter values at a time.    

Example:
If net_type is equal to ["resnet_50","resnet_101"], then 2 datasets will be created, or if maxiters is equal to [1000,2000,3000], then there will be 3 network training cycles.
(In the config file.json parameters are divided into two categories to better navigate. For more detailed information for each parameter, refer to the documentation: https://deeplabcut.github.io/DeepLabCut/docs/standardDeepLabCut_UserGuide.html#g-train-the-network )
