# Power Level vs. Active Cycles 

## Sample works / Publications include:     
- [Coupled electromagnetics, multiphase transport and large deformation model for microwave drying](https://www.sciencedirect.com/science/article/abs/pii/S0009250916304869)          
> - **dilectrcis ($\epsilon$)** functions of temperature and moisture content, and mixed using **LLLE** model.                  
> - **direct** implementation of **porosity** and **mechanics**.       
> - other thermophysical properties are **linear**.                    
> - constant pulse intervals                           
>> - Duty cycling at **10% power level** = microwave ON for 2 s and OFF for 20 s for a total cycle time of 22 s.                                  
- [Multiphase porous media model for intermittent microwave convective drying (IMCD) of food](https://www.sciencedirect.com/science/article/abs/pii/S1290072916000314)         
> - **dilectrcis ($\epsilon$)** function of moisture content.             
> - Pulse as **analytic function** shown in **Figure 2**.          
- [Microwave decontamination processing of tahini and process design considerations using a computational approach](https://www.sciencedirect.com/science/article/pii/S146685642300111X)                
> - in **Figure 6** the pulses are shown but unclear with in-text description of:     
>> - To account this, the on-off cycles were recorded during the 
experiments and applied in the model where the off-cycles had 0.001 
W to ensure the convergence in the electromagnetic field 
distribution.         
- [Microwave drying of spheres: Coupled electromagnetics-multiphase transport modeling with experimentation. Part II: Model validation and simulation results](https://www.sciencedirect.com/science/article/pii/S0960308515001030)                   
- [Microwave drying of spheres: Coupled electromagnetics-multiphase transport modeling with experimentation. Part I: Model development and experimental methodology](https://www.sciencedirect.com/science/article/pii/S0960308515001054)               
> - **dilectrcis ($\epsilon$)** functions of temperature and moisture content, and mixed using **LLLE** model.            
> - other thermophysical properties are **linear**.                 
>> -  Two **different time stepping** schemes were employed for the ON and OFF phase.             
> - pulsating implmentation not clarified.        


## **CMP Microwave Cavity**              
          
> Total Exposure Time = 60s (follows IEC 60705:2010 + A1:2014 testing protocol)                           

|   Case number     |   Total Time (s) [from - to]      |    Power Level (%)        |   Online (s) [from - to]      |   Offline (s) [from - to]     |        
|   ---             |   ---                             |   ---                     |   ---                         |   ---                         | 
|   1               |   60 [ 0:02 - 1:02  ]             |   100                     |   58 [004: - 1:02]            |   2 [0:02 - 0.04]             | 
|                   |                                   |                           |                               |                               | 
|   2               |   60 [ 0:02 - 1:02  ]             |   90                      |   11 [0:02: - 0:13]           |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   11 [0:14 - 0:25]            |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   11 [0:26 - 0:37]            |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   12 [0:37 - 0:49]            |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   11 [0:50 - 1:01]            |   xx [0:xx - 0:xx]            | 
|   3               |   60 [ 0:01 - 1:01  ]             |   80                      |   9 [0:03 - 0:12]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   10 [0:14 - 0:24]            |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   10 [0:26 - 0:36]            |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   10 [0:38 - 0:48]            |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   10 [0:50 - 1:00]            |   xx [0:xx - 0:xx]            | 
|   4               |   60 [ 0:02 - 1:02  ]             |   70                      |   8 [0:03 - 0:11]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   9 [0:14 - 0:23]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   9 [0:26 - 0:35]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   9 [0:38 - 0:47]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   9 [0:50 - 0:59]             |   xx [0:xx - 0:xx]            | 
|   5               |   60 [ 0:02 - 1:02  ]             |   60                      |   7 [0:03 - 0:10]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   8 [0:14 - 0:22]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   8 [0:26 - 0:34]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   7 [0:39 - 0:46]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   7 [0:51 - 0:58]             |   xx [0:xx - 0:xx]            | 
|   6               |   60 [ 0:00 - 1:00  ]             |   50                      |   4 [0:04 - 0:08]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   7 [0:12 - 0:19]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   7 [0:24 - 0:31]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   7 [0:36 - 0:43]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   6 [0:49 - 0:55]             |   xx [0:xx - 0:xx]            | 
|   5               |   60 [ 0:01 - 1:01  ]             |   40                      |   4 [0:03 - 0:07]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   5 [0:14 - 0:19]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   5 [0:26 - 0:31]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   6 [0:37 - 0:43]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   6 [0:49 - 0:55]             |   xx [0:xx - 0:xx]            | 
|   6               |   60 [ 0:01 - 1:01  ]             |   30                      |   4 [0:02 - 0:06]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   5 [0:13 - 0:18]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   5 [0:25 - 0:30]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   5 [0:37 - 0:42]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   4 [0:49 - 0:53]             |   xx [0:xx - 0:xx]            | 
|   7               |   60 [ 0:01 - 1:01  ]             |   20                      |   5 [0:01 - 0:06]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   5 [0:13 - 0:18]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   4 [0:25 - 0:29]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   4 [0:37 - 0:41]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   5 [0:49 - 0:54]             |   xx [0:xx - 0:xx]            | 
|   8               |   60 [ 0:01 - 1:01  ]             |   10                      |   2 [0:02 - 0:04]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   3 [0:13 - 0:16]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   3 [0:25 - 0:28]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   3 [0:37 - 0:40]             |   xx [0:xx - 0:xx]            | 
|                   |                                   |                           |   3 [0:49 - 0:52]             |   xx [0:xx - 0:xx]            | 













