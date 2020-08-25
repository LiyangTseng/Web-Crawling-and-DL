# Use web crawling to collect images data for deep learning application
### Collect images 
> <code> python3 download_images.py **keyword_1** **keyword_2**  ... **keyword_n**  </code>

Images would then be stored at 
<code> /images/**keyword** </code>

* If more than one words are given as a single keyword, they should be seperated by underscore <code> **_** </code>.

### Data preprocessing
Run <code> data_preprocessing.ipynb </code> to preprocess the collected data via web-crawling.
* Remmeber to correct the image path in the code.
### Training and Testing
Use preprocessed data to as input of <code> transfer_mydata.ipynb </code>
* Remmeber to correct the image path in the code.
