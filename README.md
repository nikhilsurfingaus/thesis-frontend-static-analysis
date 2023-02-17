# PySolSweep Frontend Display <img src="https://github.com/nikhilsurfingaus/thesis-frontend-static-analysis/blob/master/src/assets/logo.png" width="40" >
# Main Thesis Project Repo
## [ThesisProject-Static-Analysis-Solidity-Smart-Contracts](https://github.com/nikhilsurfingaus/ThesisProject-Static-Analysis-Solidity-Smart-Contracts)
# Frontend Display Demo
# Demo: [https://pysolsweep.io](https://pysolsweep.netlify.app/)
## Screenshots
<p float="left">
  <img src="https://github.com/nikhilsurfingaus/thesis-frontend-static-analysis/blob/master/src/assets/1.jpg" height=300 width="500" />
  <img src="https://github.com/nikhilsurfingaus/thesis-frontend-static-analysis/blob/master/src/assets/2.jpg" height=300 width="500" />
  <img src="https://github.com/nikhilsurfingaus/thesis-frontend-static-analysis/blob/master/src/assets/3.jpg" height=300 width="500" />
  <img src="https://github.com/nikhilsurfingaus/thesis-frontend-static-analysis/blob/master/src/assets/4.jpg" height=300 width="500" />
  <img src="https://github.com/nikhilsurfingaus/thesis-frontend-static-analysis/blob/master/src/assets/5.jpg" height=300 width="500" />
  <img src="https://github.com/nikhilsurfingaus/thesis-frontend-static-analysis/blob/master/src/assets/6.jpg" height=300 width="500" />
  <img src="https://github.com/nikhilsurfingaus/thesis-frontend-static-analysis/blob/master/src/assets/mobile.jpg" height=600 width="380" />
</p>

## Website Powered By
<img src="https://cdn.freebiesupply.com/logos/large/2x/react-1-logo-png-transparent.png" alt="drawing" width="100"/> <img 
src="https://user-images.githubusercontent.com/16843090/101181820-f3a63780-3612-11eb-9d3a-05452f2b0ad8.png" alt="drawing" width="100"/> <img src="https://camo.githubusercontent.com/394ba38797d83799a16f1cb2fd3fc8f607b9fb116f49cf1e1b64eacff9844602/68747470733a2f2f75706c6f61642e77696b696d656469612e6f72672f77696b6970656469612f636f6d6d6f6e732f7468756d622f642f64352f5461696c77696e645f4353535f4c6f676f2e7376672f3230343870782d5461696c77696e645f4353535f4c6f676f2e7376672e706e67" alt="drawing" width="100"/><img 
src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png" alt="drawing" width="100"/> <img 
src="https://user-images.githubusercontent.com/16843090/101181820-f3a63780-3612-11eb-9d3a-05452f2b0ad8.png" alt="drawing" width="100"/>

- The **React** Framework Library Web Application Crypto X Gains, can either be used in Mobile/Desktop/Tablet modes with responsive design. 

- **Tailwind.css** makes it quicker to write and maintain the application code. By using this utility-first framework, don't have to write custom CSS to style in the application. Instead, use utility classes to control the padding, margin, color, font, shadow, and more of the application.

- **Axios** is a library that serves to create HTTP requests that are present externally. This includes fetching data from both the deployed backend Express Js server which returns the results of the YTDL-Core from the parsed user URL. Axios also fetches live stats for my Github profile in the Install page using the Github REST API.

- **Python** makes it quicker to write and maintain the application code. By using this utility-first framework, don't have to write custom CSS to style in the application. Instead, use utility classes to control the padding, margin, color, font, shadow, and more of the application.

- **Solidity** makes it quicker to write and maintain the application code. By using this utility-first framework, don't have to write custom CSS to style in the application. Instead, use utility classes to control the padding, margin, color, font, shadow, and more of the application.


# Static Analysis Tool For Solidity Smart Contracts
## Intro
PySolSweep is a Static Program Analysis tool, which evaluates the securiity safety of a Solidity based Smart Contract. This tool offers coverage accross
three classes of attacks from Overflow/Underflow, Syntax and DAO. A total of 35 major bugs and their variants are detcted by the Python based
Static Analysis tool. This benefits of PySolSweep is its ability to overcome existing Solidity Static Analysis tools limitations and gaps of a 
systematic approach of Bug Attack Theme coverage of bugs rather than a randmom assortment, suggested solution to overcome bug, vulnrability or
countermeasure. As well as new bugs, vulnerbilities and countermeasures discovered from credited Academic Papers reviewed 2020-2022. The tool will
not only provide a log report of the Static Analysis results but also give a contract rating score.
## Dependencies
### Install Python
Python 3 can be installed using pip:

    python3 -m pip install -U mypy
- Debian/Ubuntu
    1. Install using [apt-get](https://linux.die.net/man/8/apt-get).
        ```sh
        $ sudo apt-get update
        $ sudo apt-get install python3
        ```
    1. Recommended - install development extensions (C headers necessary for some packages), `pip` (for installing packages globally), and `venv` (for creating a virtual environment).
        ```sh
        $ sudo apt-get install python3-dev python3-pip python3-venv
        ```
- macOS
    1. Install [Brew](https://brew.sh). 
    1. Install Python using Brew:
        ```sh
        $ brew install python3
        ```
    1. Make your the Brew executables `bin` directory is in your `PATH` variable.
- Windows
    1. Download Python from the [Windows Download](https://www.python.org/downloads/windows/) page.
    2. Run the installer.
        - Be sure to _check_ the box on to have Python added to your `PATH` if the installer offers such an option (it's normally off by default).
### Python Libraries if not already installed with your current Python Version (Python Inc All These Libraries)
#### Installing Numpy
```sh
$ pip install numpy
```
or
```sh
$ conda install numpy
```
#### Installing Tkinter
```sh
$ pip install tk
```
or
```sh
$ conda install tk
```
#### Installing Time
```sh
$ pip install python-time
```
or
```sh
$ conda install python-time
```

## Usage
### General Contract Instructions
The first static analysis mode is general scan, which covers all three Bug Attack Theme (BAT) classes of Overflow/Underflow, Syntax and DAO. The use-case involves a smart contract being placed within the ‘Verify’ subfolder. The file location would then be input as ‘Verify/filename.txt’, with the solidity code transformed into a Python readable text format. The ‘Start Scan Analysis' UI button would be selected and static analysis of the smart contract would be executed. Once completed, the results were displayed both in the terminal as well as an output text file namly ‘bugreport.txt’. 

<img src="https://github.com/nikhilsurfingaus/ThesisProject/blob/master/Resources/General.jpg" alt="General" width="600" height="400"/> 

### Withdraw Function Contract Instructions
The second static analysis mode produced was that of a DAO withdraw/transfer function scan, which covered DAO bugs and vulnerabilities specific to a smart contracts withdraw/transfer function. The use-case follows similar to the general scan with the smart contract again placed within the ‘Verify’ subfolder in a .txt
file. Then fill out details of the withdraw/transfer function including the function name, amount variable name and balance variable name. Once completed, the results were displayed both in the terminal as well as an output text file namly ‘bugreport.txt’. 

<img src="https://github.com/nikhilsurfingaus/ThesisProject/blob/master/Resources/Withdraw.jpg" alt="Withdraw" width="600" height="400"/> 

## Bugs Detected
### Overflow/Underflow Vulnerabiltiies
Num | Detector | Detection Details | Solutuion | Risk | Confidence
--- | --- | --- | --- | --- | --- |
1 | `Check Safe Math` | This check catches if a smart contract is defined using the ^ operator for compiler version. | Best practice to use static rather than dynamic compiler version as future versions could have unintended effects | Medium | High
2 | `Check Integer Operations` | This check catches if a smart contract is defined without the Safe Math Library present when using uint variable type | Best practice to use Safe Math Library which can minimise attack exploiting overflow/underflow vulnerabilities with arthimetic operations | High | High
3 | `Check Loop Condition` | This check catches if a smart contract uses arithemtic operations such as '+, -, *, /, %' when Safe Math functions could be used.  | Best practice to use Safe Math Library functions of add, sub, div, mod or mul which can minimise attack exploiting overflow/underflow vulnerabilities | Medium | High
4 | `Check Div Multiply` | This check catches if a smart contract has mathematical operations with multiplication or division, that division occurs first  | Best practice to use have multiplication first, as division first can cause loss of pecision in operations  | Medium | Medium
5 | `Check Unary` | This check catches if a smart contract contains =+, =- or =* which could be intended as =+, -= or *= | To minimise misconception be sure to use += or -= or *= | Low | High
6 | `Check Type Inference` | This check catches if a smart contract defined variable using var instead of using numerical data type of uint | Should explicitly declare uint data types to avoid unexpected behaviors | Medium | High

### Syntax Vulnerabiltiies
Num | Detector | Detection Details | Solutuion | Risk | Confidence
--- | --- | --- | --- | --- | --- |
1 | `Compiler Issue` | This check catches if a smart contract is defined using the ^ operator for compiler version. | Best practice to use static rather than dynamic compiler version as future versions could have unintended effects | Medium | High
2 | `Check Boolean Constant` | This check catches if a smart contract incorporates Boolean Constance or Tautology conditions | Should verify that Tautology is not intended as well as Constance is not indended | Low | High
3 | `Check Array Length` | This check catches if a smart contract defined an array with a static length | Should increase array length as array grows and storage neede | Medium | Medium
4 | `Check Address Zero` | This check catches if a smart contract function does not check that the address is zero using address(0), 0x0 or address(0x0) | Check address is not zero using require and address variable reduce liklihood of interaction with a null address | Medium | High
5 | `Check Map Struct Deletion` | This check catches if a smart contract either defines a map struct as a different data type or uses delete keyword for mapping delete which doesnt not delete the entire mapping only deletes entry | Should Use same data type key as defined in struct for mapping. Use lock technqiue mechanism to disable mapping structure if needed to remove | Medium | High
6 | `Check Initial Storage Variable` | This check catches if a smart contract includes struct variables which are not set when using struct | Should Immediatly initalise storage variables could be ovveridded | High | Low
7 | `Check Assemble Shift` | This check catches if a smart contract includes an assembly shift that has parameters mismatched in their order | When using shr assembly shift if first position is a variable and second is constant, this bit shift is usually unintended | Medium | Medium
8 | `Check Self Destruct` | This check catches if a smart contract contains a self destruct with address or a function that is public and uses self destruct | When address in self destruct address is not used as could send ether to an attacker contract. If using self detruct restrict access to function as not public | High | High
9 | `Check Transfer` | This check catches if a smart contract contains call.value or send value methods | Use transfer function instead of send/call operation as they don't capture transaction fails to minimise vulnerbaility | Medium | High
10 | `Check Bytes` | This check catches if a smart contract contains bytes array instead of using bytes | Use bytes instead of byte array as this could grow and access un intended storage | Low | High
11 | `Check Tx Origin` | This check catches if a smart contract contains txorigin function | Use msg.sender instead of tx.origin to minimise vulnerbaility. tx.Orgin is vulnerable for authentication as it can be manipulated to be equal to an owner address hence pass the require tests | High | High
12 | `Check Fuction Visibility` | This check catches if a smart contract contains functions with unknown visibility | Use at least minimum public/private specifier when defining function to minimise vulnerbaility | High | High
13 | `Check Balance Equality` | This check catches if a smart contract double equals for evaluation of a balance variable | Use compartive statements instead of double equals to minimise vulnerbaility | Medium | Low
14 | `Check Block Timestamp` | This check catches if a smart contract contains block.timestamp for randomness | Avoid block.randomness for randomness to minimise DoS vulnerbaility | Low | High
15 | `Check Block Variable` | This check catches if a smart contract contains block.timestamp/gaslimit or difficulty | Potenital leaky PRNGS rely heavily on past block hashes future vulnerbility | Low | High
16 | `Check Block Number` | This check catches if a smart contract contains block.number | Check function when getting current block number could be invoked by an attacker for malicious intent | Low | High
17 | `Check Block Gas` | This check catches if a contract contains for/while loops which conditionuses the length of an array or object to iterate over | Avoid loop of unknown size that could grow and cause DoS vulnerability | Medium | High
18 | `Check Delegate Call` | This check catches if a delegate call is made, potential for parity sig wallet attack | Avoid Delegate Call this can lead to unexpected code execution vulnerbaility | Medium | High
19 | `Check Loop Function` | This check catches if a function call is made within a for or while loop | Avoid Function Call In For/While Loop possible DoS vulnerbaility | Medium | High
20 | `Check Owner Power` | This check catches if a contract bases function control and execution on the owner. Or a modifier function is used to define an owner. | Owner private key at risk of being comprimised don't base function control on owner or use an owner modifier function | High | Medium
21 | `Check Constructor Initialise` | This check catches if a contract defines multiple constructors either through constructor or a function constructor. Checks wether same variables are defined over multiple constructors could be overwritten.  | Use single constructor to initialise contract second constructor  will be ignoreded. Use single constructor and intialise variables once in constructor | Low | Medium
22 | `Check Local Variable Shadowing` | This check catches if a contract contains the phenomanum of local variable shadowing. This includes the local variable shadows an instance variable in the outerscope based in the modifier, struct, function, constructor and mapping. | Consider renaming local function variable to mitigate unintended local variable shadowing or Consider not redefining contract local variables variable unless inteded to. | Low | Medium
23 | `Check State Variable Shadowing` | This check catches if a contract contains the phenomanum of state variable shadowing. This includes using and refdefing inherited variables from the parent contract in the child contract | Solutions include assign Parent Contract prior to child contract. Define inherited parent contract variable in Constructor. Same variable name from parent redefined use different variable name. Parent contract variable never assigned, assign in parent contract to prevent | High | Medium
24 | `Check Fallback` | This check catches if a contract contains an external Fallback function for transfer of ether. Without being marked as payable contract could through error and be inactive without this component | Mark Fallback function with payable otherwise contract cannot recieve ether | Medium | Medium

### DAO Vulnerabiltiies
Num | Detector | Detection Details | Solutuion | Risk | Confidence
--- | --- | --- | --- | --- | --- |
1 | `Check Contract Lock` | This check checks wether a contract contains a lock modifier for reentracy attack. As well as wether conditions of require, true condition guard for reentracy conditions by checking external calls that are unprotected.  | Use a blockreentracy contract lock mechanism so only a single contract function is executed | Medium | Medium
2 | `Check Require` | This check checks wether a contract with the withdraw function conducts a require verfication of amount and balance state variable to ensure funds are not in correctly extracted by an attacker  | Condition need this to check require balance and amount first before any operations in withdraw function | Medium | Medium
3 | `Check State Variable Update` | This check checks wether a contract with the withdraw function conducts an update to the Balance state variable prior to any operations such as call, send or transfer.  | Condition to Update state variable before call to prevent reetrancy multiple calls from attacker   | High | Medium
4 | `Check External Call` | This check checks wether a contract that calls an external function from another contract is marked as either trusted or untrusted. If untrusted this could be vulnerable to an attack invoked by the adversary. | Be aware that subsequent calls also inherit untrust state. Unknown trust, label function either trusted/untrusted | High | High
5 | `Check Effect Interacts Pattern` | This check checks wether a contract with the withdraw function conducts the Checks-effects-interactions pattern when withdrawing funds from the balance. This pattern can ensure that all prerequiestes  before executing a the entire withdrawal. This pattern will prevent reclusive calls by managing the reentracy state. | Incoporate the Check-Effect-Interacts pattern, ensure that order is correct. Inlcuding all three components will act as a reentracy gaurd. However if out of order, contract withdraw function could still be vulnerable to DAO reentracy attack.  | High | Medium

## Contributions
The significance and contributions of this project on the static analysis of solidity smart contracts was immense. The first major contribution was that of the Control Flow Diagrams (CFD’s) constructed. These CFD’s extended the logic of 11 existing parse tree infrastures, as well as proposed 23 new CFD logic for parse tree infrastures. The evaluation and testing of this CFD logic through a group consensus with multiple other static tools. Validated the credibility of its violation path logic for usage as parse trees in bug and vulnerability detection.  Other significant contributions include that of the proposed approach of bug, vulnerability and countermeasures detected being based on Bug Attack Theme (BAT) coverage. The project demonstrated this approach towards program analysis of determining which bugs and vulnerabilities induce which attack theme, then detect all bugs, vulnerabilities and countermeasures within that attack theme. The experiment evaluation conducted supported this notion, as well as unearthing multiple general insights of existing Solidity Static Analysis tools and Ethereum blockchain deployed smart contractors.  Contributions from the evaluation included the lack of coverage existing static analysis tools provide against core attacks such as Overflow/Underflow, Syntax and DAO. Illustrating the impact of new bugs and vulnerabilities discovered in academic papers, and the lack of detection in tools which were released prior to these new bugs and vulnerabilities. The evaluation moreover illuminated a worrying insight into the large volume of medium to high risk impact bugs and vulnerabilities present in Ethereum blockchain deployed smart contracts. Thus, the significance and contributions of this project furthered the knowledge and research in the field of static analysis on Solidity Smart Contracts.

## References
"Program Analysis - Wikipedia", En.wikipedia.org, 2021. [Online]. Available: 
https://en.wikipedia.org/wiki/Program_Analysis. [Accessed: 19- Aug- 2021].

R. Bellairs, "What Is Static Analysis? Static Code Analysis Overview | Perforce Software", 
Perforce Software, 2021. [Online]. Available: https://www.perforce.com/blog/sca/what-Static￾Analysis. [Accessed: 19- Aug- 2021].

"Security Tools - Ethereum Smart Contract Best Practices", Consensys.github.io, 2021. 
[Online]. Available: https://consensys.github.io/Smart-Contract-best-practices/security_tools/. 
[Accessed: 19- Aug- 2021].

"Security testing - Wikipedia", En.wikipedia.org, 2021. [Online]. Available: 
https://en.wikipedia.org/wiki/Security_testing. [Accessed: 19- Aug- 2021].

"What Is Ethereum?", Investopedia, 2021. [Online]. Available: 
https://www.investopedia.com/terms/e/ethereum.asp. [Accessed: 19- Aug- 2021].

G. McCubbin, "The Ultimate Ethereum Dapp Tutorial (How to Build a Full Stack 
Decentralized Application Step-By-Step) | Dapp University", Dapp University, 2021. [Online]. 
Available: https://www.dappuniversity.com/articles/the-ultimate-ethereum-dapp-tutorial. 
[Accessed: 19- Aug- 2021].

L. Mearian, "What's a Smart Contract (and how does it work)?", Computerworld, 2021. 
[Online]. Available: https://www.computerworld.com/article/3412140/whats-a-Smart-Contract￾and-how-does-it-work.html. [Accessed: 19- Aug- 2021].

"Ethereum price today, ETH live marketcap, chart, and info | CoinMarketCap", 
CoinMarketCap, 2021. [Online]. Available: https://coinmarketcap.com/currencies/ethereum/. 
[Accessed: 19- Aug- 2021].

"Smart Contract Security: What Are the Weak Spots of Ethereum, EOS, and NEO 
Networks?", TechNative, 2021. [Online]. Available: https://technative.io/Smart-Contract￾security-what-are-the-weak-spots-of-ethereum-eos-and-neo-networks/. [Accessed: 19- Aug-2021].

"The Landscape of Solidity Smart Contract Security Tools in 2020", Kleros, 2021. [Online]. 
Available: https://blog.kleros.io/the-landscape-of-Solidity-Smart-Contract-security-tools-in-
2020/. [Accessed: 19- Aug- 2021].


E. Attacks.md, "Ethereum Attacks.md", Gist, 2021. [Online]. Available: 
https://gist.github.com/ethanbennett/7396bf3f61dd985d3426f2ee184d8822. [Accessed: 19- Aug-
2021].

A. John and T. Westbrook, "Crypto platform Poly Network rewards hacker with $500,000 
'bug bounty'", Reuters, 2021. [Online]. Available: https://www.reuters.com/technology/crypto￾platform-poly-network-rewards-hacker-with-500000-bug-bounty-2021-08-13/. [Accessed: 19-Aug- 2021].

"Static Analysis of Integer Overflow of Smart Contracts in Ethereum | Proceedings of the 
2020 4th International Conference on Cryptography, Security and Privacy", Dl.acm.org, 2021. 
[Online]. Available: https://dl.acm.org/doi/abs/10.1145/3377644.3377650. [Accessed: 19- Aug-2021].

"SmartCheck: Static Analysis of Ethereum Smart Contracts", Ieeexplore.ieee.org, 2021. 
[Online]. Available: https://ieeexplore.ieee.org/document/8445052. [Accessed: 19- Aug- 2021].

P. Praitheeshan, L. Pan, J. Yu, J. Liu and R. Doss, "Security Analysis Methods on Ethereum 
Smart Contract Vulnerabilities: A Survey", arXiv.org, 2021. [Online]. Available: 
https://arxiv.org/abs/1908.08605. [Accessed: 19- Aug- 2021].

"ÆGIS: Shielding Vulnerable Smart Contracts Against Attacks | Proceedings of the 15th 
ACM Asia Conference on Computer and Communications Security", Dl.acm.org, 2021. 
[Online]. Available: https://dl.acm.org/doi/abs/10.1145/3320269.3384756. [Accessed: 19- Aug-2021].

"How effective are Smart Contract Analysis tools? evaluating Smart Contract Static Analysis
tools using bug injection | Proceedings of the 29th ACM SIGSOFT International Symposium on 
Software Testing and Analysis", Dl.acm.org, 2021. [Online]. Available: 
https://dl.acm.org/doi/10.1145/3395363.3397385. [Accessed: 19- Aug- 2021].

"Smart Contract: Attacks and Protections", Ieeexplore.ieee.org, 2021. [Online]. Available: 
https://ieeexplore.ieee.org/document/8976179. [Accessed: 19- Aug- 2021].

H. Preston, "Integer overflow and underflow vulnerabilities - Infosec Resources", Infosec 
Resources, 2020. [Online]. Available: https://resources.infosecinstitute.com/topic/integer￾overflow-and-underflow-vulnerabilities/. [Accessed: 01- Jun- 2022].

D. Siegel, "Ethereum Understanding The DAO Attack", CoinDesk, 2022. [Online]. 
Available: https://www.coindesk.com/learn/2016/06/25/understanding-the-dao-attack/. 
[Accessed: 01- Jun- 2022].

J. Wu, "Ethereum’s History: From Zero to 2.0", WisdomTree, 2021. [Online]. Available: 
https://www.wisdomtree.com/blog/2021-07-15/ethereums-history-from-zero-to-20. [Accessed: 
01- Jun- 2022].

M. Staderini, A. Pataricza and A. Bondavalli, "Security Evaluation and Improvement of 
Solidity Smart Contracts", SSRN, 2022. [Online]. Available: 
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4038087. [Accessed: 01- Jun- 2022].

"Solidity Scan", Docs.Solidityscan.com, 2022. [Online]. Available: 
https://docs.Solidityscan.com/. [Accessed: 01- Jun- 2022].

"GitHub - Smartdec/Smartcheck: SmartCheck – a Static Analysis tool that detects 
vulnerabilities and bugs in Solidity programs (Ethereum-based Smart Contracts).", GitHub, 
2019. [Online]. Available: https://github.com/Smartdec/Smartcheck. [Accessed: 01- Jun- 2022].
2020. 
"ContractGuard - Testing Platform for Smart Contracts", Contract.guardstrike.com, 2019. 
[Online]. Available: https://Contract.guardstrike.com/. [Accessed: 11- Jun- 2022].

"Security Considerations — Solidity 0.6.11 documentation", Docs.Soliditylang.org, 2020. 
[Online]. Available: https://docs.Soliditylang.org/en/v0.6.11/security-considerations.html. 
[Accessed: 05- Jun- 2022].

"GitHub - SilentCicero/solint: A linting utility for Ethereum Solidity Smart￾Contracts", GitHub, 2019. [Online]. Available: https://github.com/SilentCicero/solint. 
[Accessed: 06- Jun- 2022].

"remix-project/libs/remix-analyzer at master · ethereum/remix-project", GitHub, 2020. 
[Online]. Available: https://github.com/ethereum/remix-project/tree/master/libs/remix￾analyzer#readme. [Accessed: 08- Jun- 2022].
