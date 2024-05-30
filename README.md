# UDrive Benchmark Part One #
## Part of Submission to NeurIPS 2024 Dataset and Benchmark Track #
### Results and code are in the analysis folder ###
Steps to reproduce the image analysis results:
- Visit the Fine-tuned GPT Model at: https://chatgpt.com/g/g-Rpba6Wp9Q-drive-scene-analyzer
- Select any image in the analysis folder under Argoverse1. Or, you may choose your own images.
- observe results
Steps to reproduce the dataset analysis results:
- Download the code
- Comment/Uncomment the following code:
- Create network class: ```G = DatasetAnalysis()```
- Create a network graph representation based on the analysis JSON file: ```G.createBasicGraph()```
- Calculate scenario level results: ```G.compareScenarios()```
- Calculate image level results: ```G.compareImages(0.8)```
- Calculate degree centrality: ```G.calculateDegreeCentrality(10)```
- Create a random graph and perform the analysis: ```G.randomAnalysis()```
- Store the randomly generated graph: ```G.createRandomDataset()```
