Measuring the Accuracy of Password Strength Meters
================================

Password strength meters are an important tool to help users choose more secure passwords.
However, strength meters can only then provide reasonable guidance when they are accurate, i.e., their score correctly reflects password strength.
A strength meter with low accuracy may do more harm than good and guide the user to choose passwords with a high score but actual low security.

The preferred method to measure the accuracy of a strength meter is to compare it to an ideal _reference_, measuring the similarity between the reference and _the meter output_.
In our work, [On the Accuracy of Password Strength Meters](https://maximiliangolla.com/files/2018/papers/ccsf285-finalv3.pdf), we found the **weighted [Spearman's rank correlation coefficient](https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient)** to be a useful candidate to measure the accuracy of a strength meter compared to the ideal reference.

In this repository you find the necessary code to crawl and evaluate a password strength meter's accuracy.
We hope that this code is helpful for meter developers to improve their implementation.

Related Work
-----------
* Follow-up work (2023): [No Single Silver Bullet: Measuring the Accuracy of Password Strength Meters](https://www.usenix.org/conference/usenixsecurity23/presentation/wang-ding-silver-bullet)
* Prior work (2014): [From Very Weak to Very Strong: Analyzing Password-Strength Meters](https://www.ndss-symposium.org/ndss2014/programme/very-weak-very-strong-analyzing-password-strength-meters/)

Project Website
-----------
The original paper, a recording of the talk, the slides, and more information can be found at:

* https://password-meter-comparison.org

User Guide
-----------
The code consists of three parts: `crawler`, `post-processing`, and `evaluation`.
As the crawler uses the [**Selenium framework**](https://www.seleniumhq.org), we automate a headless Google Chrome/Mozilla Firefox browser to crawl a meter using some predefined list of passwords.
In a post-processing step we use a small **Python** script to prepare the crawled data for the evaluation step in **R**.
In the final step, we calculate the weighted Spearman correlation to estimate the accuracy of the crawled meter.

### Obtaining an Ideal _Reference_
While this repository contains some example passwords from the LinkedIn leak, a more evolved evaluation requires more than one ground truth. The easiest way to obtain such references is by sampling passwords from password leaks, and evaluating them using [CMU's Password Guessability Service (PGS)](https://pgs.ece.cmu.edu). For more details please refer to [the paper](https://maximiliangolla.com/files/2018/papers/ccsf285-finalv3.pdf).

### Installation

To keep the guide short, we assume the use of [Ubuntu 22.04 LTS](https://xubuntu.org/release/22-04/).
All `Python` code snippets were tested using **3.10**, all `R` scripts assume version **4.3** or later.

Check out the source code via:

`$ git clone https://github.com/RUB-SysSec/Password-Strength-Meter-Accuracy.git PSMA`

```
.
└── src
    ├── analyze
    │   ├── 01_build_r_file.py
    │   └── 02_corr-comp.r
    ├── crawl
    │   └── 01_zxcvbn
    │       ├── zxcvbn_chrome.py
    │       └── zxcvbn_firefox.py
    ├── datasets
    │   ├── offline
    │   │   ├── 0_linkedin.offline.pw
    │   │   ├── 1_linkedin.offline.strength
    │   │   ├── 2_linkedin.offline.weight
    │   │   └── 3_linkedin.offline.withcount
    │   └── online
    │       ├── 0_linkedin.online.pw
    │       ├── 1_linkedin.online.strength
    │       ├── 2_linkedin.online.weight
    │       └── 3_linkedin.online.withcount
    └── meter
        └── 01_zxcvbn
            ├── index.html
            └── zxcvbn_v4.4.2.js
```
#### Step 0: Preparation

Before we start, we need to install some dependencies, like Python PIP, Selenium, and a WebDriver for your browser.

###### Configuring Python and Installing Selenium
First we install Python [Package Installer](https://pip.pypa.io/en/stable/) (PIP) and the Python [virtual environment](https://docs.python.org/3.10/glossary.html#term-virtual-environment) runtime environment.

`$ sudo apt-get install python3-pip python3-virtualenv`

We start by creating a new Python virtual environment that we just use for this project.

`$ virtualenv -p /usr/bin/python3 venv`

Next, we activate the Python virtual environment.

`$ source venv/bin/activate`

Now, we install selenium.

`(venv) $ pip install selenium`

###### Installing the WebDriver

By default, ***Ubuntu 22.04 LTS*** ships [Firefox as a Snap package](https://snapcraft.io/firefox), which causes a lot of [issues](https://github.com/SeleniumHQ/selenium/issues/11028) with the geckodriver.

We need to replace Firefox Snap with the Debian (deb) package, for this you best follow [the detailed tutorial from OMG! Ubuntu!](https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04).

To allow Selenium to communicate and automate your browser, we also need to install your web browser's driver.

`(venv) $ pip install webdriver-manager`

###### Installing R

Install the [R open-source programming language](https://www.digitalocean.com/community/tutorials/how-to-install-r-on-ubuntu-22-04) on your Ubuntu machine.

Optional: Install [RStudio Desktop](https://posit.co/download/rstudio-desktop/) for more convenience.

#### Step 1: Crawling the Meter
In a first step, we need to get the estimates from the strength meter for a given set of passwords.
For most web-based password strength meters we need the Selenium framework and a web browser (and its WebDriver!) to obtain such estimates.
Our tutorial includes an example based on the [zxcvbn strength meter](https://github.com/dropbox/zxcvbn).

While we try to explain everything in detail, we skip the part on how to install a web browser on your system, just use [Google Chrome](https://www.google.com/chrome/) or [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/).

Note: If your meter is not a web-based strength meter, you need write some custom function that will output strength estimates for a given list of passwords found in the `datasets` folder.

Navigate to `src/meter/01_zxcvbn/` and open `index.html` with your browser. Copy the path that is displayed in the URL bar, likely similar to:

`file:///home/<username>/PSMA/src/meter/01_zxcvbn/index.html`

Now edit `src/crawl/01_zxcvbn/zxcvbn_chrome.py` or `src/crawl/01_zxcvbn/zxcvbn_firefox.py` and change the path according to your environment.

```
...
    driver.get('file:///home/<username>/PSMA/src/meter/01_zxcvbn/index.html')
...
```

Save your edits!

Next, we make sure that the Python virtual environment is activated, and we change the current directory to `src/crawl/01_zxcvbn/`.

```
$ cd src/crawl/01_zxcvbn/
$ source ~/venv/bin/activate
(venv) $ python zxcvbn_chrome.py ../../datasets/online/0_linkedin.online.pw
```

![Alt text](/docs/screenshots/zxcvbn.gif?raw=true "zxcvbn Crawling in Action")

#### Step 2: Post-Processing

First, navigate to `src/analyze/` and edit `01_build_r_file.py` to your needs.

On the Terminal run:

```
$ cd src/analyze/
$ python 01_build_r_file.py
```

It will produce 2 files:
* `result_online.csv`
* `result_offline.csv`

Contents of `result_online.csv`:
```
password      strength       weight    count    zxcvbn_guess_number    zxcvbn_score
123456      -1044164.0    1044164.0     30.0                    2.0             0.0
linkedin     -193001.0     193001.0      6.0                22802.0             1.0
password     -176120.0     176120.0      4.0                    3.0             0.0
111111        -78720.0      78720.0      4.0                    9.0             0.0
...
```

#### Step 3: Evaluation using R

On Ubuntu 22.04 we need to install GNU Fortran

`$ sudo apt install gfortran`

and the Linear Algebra PACKage (LAPACK) and the Basic Linear Algebra Subprograms (BLAS):

`$ sudo apt-get install libblas-dev liblapack-dev`

Next, you can start R, e.g., by running RStudio or `R`:

`> install.packages("wCorr")`

This installs the support for Weighted Correlations in R.

In R run `02_corr-comp.r`, e.g., by running:

`$ Rscript 02_corr-comp.r`

The output for `result_online.csv`:
```
zxcvbn_guess_number    0.802
zxcvbn_score           0.376

# -1.0 means strong negative correlation; meter works but 'strong' passwords are in fact 'weak' and the other way round
#  0.0 means no correlation; meter is randomly guessing, and not estimating password strength
#  1.0 means strong positive correlation; meter works perfectly
```

Now edit `02_corr-comp.r` and change the input file to `"result_offline.csv"`.

The output for `result_offline.csv`:
```
xcvbn_guess_number    0.908
zxcvbn_score          0.670

# -1.0 means strong negative correlation; meter works but 'strong' passwords are in fact 'weak' and the other way round
#  0.0 means no correlation; meter is randomly guessing, and not estimating password strength
#  1.0 means strong positive correlation; meter works perfectly
```

FAQ
---

* The crawling does not work!
Make sure you have activated the virtual environment. Check for the presence of the `(venv)` in front of your prompt.
Make sure you have the latest WebDriver installed on your system.

License
-------

Our code in the **Password-Strength-Meter-Accuracy** repository is licensed under the MIT license.
Refer to [docs/LICENSE](docs/LICENSE) for more information.

### Third-Party Libraries
* **zxcvbn** is a password strength meter developed by Daniel Wheeler and Dropbox, Inc. and is using the MIT license.
The license can be found [here](https://github.com/dropbox/zxcvbn/blob/master/LICENSE.txt).
* **jQuery** is a JavaScript library developed by the JS Foundation and is using the MIT license.
The license can be found [here](https://jquery.org/license/).
* **wCorr** is an R package developed by Ahmad Emad and Paul Bailey and is using the GPL-2 license.
The license can be found [here](https://cran.r-project.org/web/licenses/GPL-2).
* **Selenium** is a browser automation framework developed by ThoughtWorks and is using the Apache 2.0 license.
The license can be found [here](https://www.apache.org/licenses/LICENSE-2.0).

Contact
-------
Visit our [website](https://informatik.rub.de/mobsec/) and follow us on [Twitter](https://twitter.com/hgi_bochum).
If you are interested in passwords, consider to contribute and to attend the [International Conference on Passwords (PASSWORDS)](https://passwordscon.org).
