# Thesis Project PySolSweep <img src="https://github.com/nikhilsurfingaus/ThesisProject/blob/master/Resources/img.ico" width="70" height="70">
## Static Analysis Tool For Solidity Smart Contracts
## Intro
TODO
## Dependicies
TODO
## Usage
### Standard Contract
TODO
### Withdraw Function
TODO
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
TODO
## References
TODO
