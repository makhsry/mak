
# Raman Spectroscopy for Mineral Detection and Sorting

<details open>  

<summary>details</summary>    

## Summary 
A critical aspect of mineral processing is selecting the appropriate technique to extract minerals from mined ore, which heavily relies on accurate species identification. This task can be challenging even for experienced professionals—minerals like chalcopyrite, pyrite, and gold can be easily mistaken for each other due to their similar visual appearances (e.g., yellowish color with metallic luster). Such misidentifications can lead to incorrect processing choices, such as using flotation to extract non-existent species, resulting in substantial financial, material, and time losses. This issue is exacerbated with low-grade ore samples, which are increasingly common due to continuous mineral exploration and the declining grades and availability of mineral resources.
The aim is to develop digital twins—high-fidelity computational models that replicate physical materials and processes. These models can be deployed at mining sites for the smart identification of mineral species and the selection of appropriate extraction processes.

Electromagnetic spectra and Raman spectra (fingerprints) will be used to identify species in mined ore samples. Currently, two comprehensive sets of spectral fingerprints exist:

- Elemental spectra: Hosted at NIST's Standard Reference Database -- Atomic Spectra Database (ASD); these spectra are unique for all known elements.
- Mineral spectra: Available from the U.S. Geological Survey Data Series and NASA's Jet Propulsion Laboratory, although discrepancies exist depending on factors such as mine location and purity/contamination.
                      
### Milestone 1: Investigating Discrepancies          
    
We will examine the fundamental building blocks of minerals—atoms—and their unique spectral fingerprints. By correlating the elemental spectra from ASD with mineral spectra, we aim to understand and account for discrepancies.

Using an Extended Iterative Optimization Technique (EIOT), we will extract intrinsic (constant) and non-intrinsic (variable) features from the spectra. Principal Component Analysis (PCA) will identify the most relevant components while maintaining a high data correlation ($>99\%$).

### Milestone 2: Developing Transferable Machine Learning Models      
          
Current mineral identification methods using hyperspectral sensors rely on supervised machine learning, which requires labeled data. This is limited by:

- The need to retrain models for each mine location,
- The inability to handle previously unseen mineral species.
               
We propose developing **unsupervised, physically informed machine learning models** that adapt to new data on-the-fly.

### Milestone 3: Building a Design Space for Single Species        
           
We will compile data on minerals of concern at Canadian mine sites, including their phase structures, transitions, and electromagnetic spectra. When data is lacking, we will use Density Functional Theory (DFT) and Molecular Dynamics (MD) to compute spectra.

This dataset will train a Convolutional Neural Network (CNN), which will be validated using a separate test dataset.

### Milestone 4: Creating Realistic Design Spaces      
   
While a CNN trained on pure species data can identify individual minerals, it may struggle with mixtures. To address this:

- Mixture models of the collected species will be developed,
- Random configurations will be generated and their spectra computed using Machine Learning Interatomic Potentials (MLIP) in MD,
- A CNN trained on these mixture datasets will be tested with experimentally collected hyperspectral images.   

         
### Milestone 5: Enabling Deployment     
          
We will explore the development of a low-cost, fast, cloud-based self-learning model for mineral detection called \textbf{otfMLesf} (on-the-fly Machine Learning models for electromagnetic spectrum fingerprints).     

- The model will use the CNN from Milestone 3 to detect single species in real-time,
- For mixtures involving detected species, it will recall the CNN from Milestone 4 to quantify composition,
- For unknown species, it will build random mixture models, compute spectra as in Milestone 4, retrain the CNN, and proceed to quantification.  

      
This work aims to revolutionize mineral identification at mine operations through the development of robust digital twins and advanced machine learning models, ensuring efficient and accurate resource extraction with minimal waste.     

### Supporting Information                

- [Automatic materials characterization from infrared spectra using convolutional neural networks](https://doi.org/10.1039/D2SC05892H)

  > <img width="2032" height="1042" alt="Image" src="https://github.com/user-attachments/assets/15a8689d-b1f8-4e49-85a3-213bd79522c2" />
- [Leveraging infrared spectroscopy for automated structure elucidation](https://www.nature.com/articles/s42004-024-01341-w)

  > <img width="777" height="662" alt="Image" src="https://github.com/user-attachments/assets/40175a5e-165f-4592-9cd9-a73e0bce80f2" />

- [On the interplay of the potential energy and dipole moment surfaces in controlling the infrared activity of liquid water](https://doi.org/10.1063/1.4916629)

  > the infrared (IR) spectrum of a generic molecular system can be obtained, within the electric dipole approximation and linear response theory, from the Fourier transform of the quantum time autocorrelation function of the system’s dipole moment
  >> <img width="798" height="142" alt="Image" src="https://github.com/user-attachments/assets/2b4c5c5e-b5af-42d6-b315-4a3dd46e61ea" />

- [Raman spectroscopy of minerals and mineral pigments in archaeometry](https://doi.org/10.1002/jrs.4914)

  > <img width="648" height="669" alt="image" src="https://github.com/user-attachments/assets/7c62442d-76e9-4fb6-913a-1f76b790d22d" />

- [Stand-off Raman spectroscopic detection of minerals on planetary surfaces](https://doi.org/10.1016/S1386-1425(03)00080-5)

  > <img width="214" height="233" alt="image" src="https://github.com/user-attachments/assets/03b135e6-3517-43a1-8d7e-9838a87c4dfd" />

- [RRUFF - Comprehensive Database of Mineral Data](https://www.rruff.net/) ([old website](https://rruff.info/about/about_IMA_list.php))

- [Mindat.org is the world's largest open database of minerals, rocks, meteorites and the localities they come from](https://www.mindat.org/)
  
- [Raman spectroscopy for mineral identification and quantification for in situ planetary surface analysis: A point count](https://doi.org/10.1029/97JE01694)

  > <img width="468" height="766" alt="image" src="https://github.com/user-attachments/assets/7b6c7469-5c69-4250-9b5d-8ec102502c51" />

</details>