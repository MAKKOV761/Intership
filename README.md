# DEEPLABCUT analays
What does this code do:
This code is designed to easily check the performance of different parameters for network training.

How to use the code:
To begin with, you need to have a project with labeled data, if there is no such, then you need to create a project and label frames. Then open the file config.json and in labeled_project_path specify the path to your project. After that, specify the desired values in the parameters in one of two categories: create_training_dataset and train_network (the recommendation in maxiters is to set a small value, especially if you have a weak PC. This will avoid eternal loading). and run dlc_analays.py via cmd.

IMPORTANT:                                                                          
Put all the values in the parameters exclusively in the [ ] lists to avoid errors. This is also necessary in order to check different parameter values at a time.

Example:
If net_type is equal to ["resnet_50","resnet_101"], then 2 datasets will be created, or if maxiters is equal to [1000,2000,3000], then there will be 3 network training cycles. Also, if several values in several parameters are specified in one category, then the number of these values will be multiplied by each other. If net_type is equal to ["resnet_50","resnet_101"], and augmenter_type is equal to ["scalecrop","imgaug"], then 4 datasets will be made (2*2=4).
(In the config file.json parameters are divided into two categories to better navigate. For more detailed information for each parameter, refer to the documentation: https://deeplabcut.github.io/DeepLabCut/docs/standardDeepLabCut_UserGuide.html#g-train-the-network )

What doesn't work yet:
1. modelprefix in train_network
2. Analaysing the results
