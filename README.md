# Opt_PredLLPS
## About Opt_PredLLPS
We develop a two-task predictor named Opt_PredLLPS for discovering potential phase separation proteins and further judge its mechanism. The first task model of Opt_PredLLPS is based on the combination of CNN and BiLSTM through fully connected layer, in which CNN uses evolutionary information features as input, and BiLSTM uses multimodal features as input, respectively. If a protein is predicted as a PS protein, then it is input into the second task model to predict whether this protein interact with partners to undergo PS. The second task model is based on XGBoost classification algorithm and 37 physicochemical properties after 3-step feature selection.

The datasets can be found in `./datasets/`. The Opt_PredLLPS models is available in `./model/`. The prediction code can be found in `Opt_PredLLPS.py, Opt_PredLLPS_Self.py and Opt_PredLLPS_Part.py.`

## Tools<bar>
The pssm feature is obtained from POSSUM. Please ensure that the fasta file submitted to POSSUM is the same as the fasta file submitted this time. POSSUM's web site is https://possum.erc.monash.edu.

 >1.The submitted sequence length should be no less than 50 and no longer than 5000.<br>
 >2.The number of sequences submitted is within 500.<br>
 >3.Submit A sequence of one and only 20 kinds of amino acids, including 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'.<br>
<br>
HMM features requires a multiple sequence alignment tools and a database. Code for generating HMM features is located in ./utils/hhblits_search.

>1.hhblits: It is an efficient protein sequence alignment tool that can quickly search homologous sequences in large databases.<br>
>2.uniclust30_2018_08: You can download it dababase from `https://wwwuser.gwdg.de/~compbiol/uniclust/2018_08/uniclust30_2018_08_hhsuite.tar.gz `.<br>

## Requirements<bar>
```
•python==3.7
•numpy==1.21.5
•Pandas==1.3.5
•scikit-learn==1.0.2
•tensorflow==1.14.0
•hhblits ==3.3.0
```
## Usage
### Running Predictions(Opt_PredLLPS.py)
• Input: The script takes an input file in FASTA format.<br>
• Output: Generates an output file. The prediction results will be saved in Opt_PredLLPS prediction results.csv.<br>
• Interpreting Scores: If the first task model scores of a protein are high (>=0.5), it is considered a LLPS protein. If the second task model scores of a protein are high (>=0.5), it is considered a PS-Self protein.<br>

### Running Predictions(Opt_PredLLPS_Self.py)
• Input: The script takes an input file in FASTA format.<br>
• Output: Generates an output file. The prediction results will be saved in Opt_PredLLPS_Self prediction results.csv.<br>
• Interpreting Scores: If scores of a protein are high (>=0.5), it is considered a PS-Self protein.<br>

### Running Predictions(Opt_PredLLPS_Part.py)
• Input: The script takes an input file in FASTA format.<br>
• Output: Generates an output file. The prediction results will be saved in Opt_PredLLPS_Part prediction results.csv.<br>
• Interpreting Scores: If scores of a protein are high (>=0.5), it is considered a PS-Part protein.<br>

## example
Simply run:<br>
```
 python Opt_PredLLPS.py --input_fasta_file test/9 proteins/test.fasta
```
And the prediction results will be saved in `Opt_PredLLPS prediction results.csv`.
