pragma solidity >=0.8.3;

contract ApolloDAO is Context {

    Token public immutable apolloToken;

    event newDaoNomination(address indexed newDAO, address indexed nominator);

    struct newDAONomination {
    uint256 timeOfNomination;
    address nominator;
    uint256 votesFor;
    uint256 votesAgainst;
    bool votingClosed;
    }

    struct DAOVotes {
        uint256 voteCount;
        bool votedFor;
    }

    mapping (address => newDAONomination) private _newDAONominations;
    mapping (address => mapping (address => DAOVotes)) private _lockedVotes;

    uint256 public constant daoVotingDuration = 259200;
    uint256 public constant minimumDAOBalance = 14000000000 * 10**9;
    uint256 public totalLockedVotes;
    uint256 public activeDaoNominations;

    address public approvedNewDAO = address(0);
    uint256 public constant daoUpdateDelay = 86400;
    uint256 public daoApprovedTime;
    uint256 public constant daoVoteBurnPercentage = 1;

    address public immutable daoAdministrator;


    constructor (address tokenAddress, address administrator) {
        apolloToken = Token(tokenAddress);
        daoAdministrator = administrator;
    }


    function voteForDAONomination(uint256 voteAmount, address newDAO, bool voteFor) external {
        require(_newDAONominations[newDAO].timeOfNomination > 0 , "There is no DAO Nomination for this address");
        require(_lockedVotes[_msgSender()][newDAO].voteCount == 0, "User already voted on this nomination");
        require(approvedNewDAO == address(0), "There is already an approved new DAO");
        apolloToken.transferFrom(_msgSender(), address(this), voteAmount);
        totalLockedVotes += voteAmount;
        _lockedVotes[_msgSender()][newDAO].voteCount += voteAmount;
        _lockedVotes[_msgSender()][newDAO].votedFor = voteFor;
        if(voteFor){
            _newDAONominations[newDAO].votesFor += voteAmount;
        } else {
            _newDAONominations[newDAO].votesAgainst += voteAmount;
        }
    }

    function withdrawNewDAOVotes(address newDAO) external {
        uint256 currentVoteCount = _lockedVotes[_msgSender()][newDAO].voteCount;
        require(currentVoteCount > 0 , "You have not cast votes for this nomination");
        require((totalLockedVotes - currentVoteCount) >= 0, "Withdrawing would take DAO balance below expected rewards amount");

        uint256 apolloToBurn = currentVoteCount * daoVoteBurnPercentage / 100;
        uint256 apolloToTransfer = currentVoteCount - apolloToBurn;

        apolloToken.transfer(_msgSender(), apolloToTransfer);
        apolloToken.burn(apolloToBurn);

        totalLockedVotes -= currentVoteCount;
        _lockedVotes[_msgSender()][newDAO].voteCount -= currentVoteCount;

        if(_lockedVotes[_msgSender()][newDAO].votedFor){
            _newDAONominations[newDAO].votesFor -= currentVoteCount;
        } else {
            _newDAONominations[newDAO].votesAgainst -= currentVoteCount;
        }

    }

    function nominateNewDAO(address newDAO) external {
        require(apolloToken.balanceOf(_msgSender()) >= minimumDAOBalance , "Nominator does not own enough APOOLLO");
        _newDAONominations[newDAO] = newDAONomination(
            {
                timeOfNomination: block.timestamp,
                nominator: _msgSender(),
                votesFor: 0,
                votesAgainst: 0,
                votingClosed: false
            }
        );
        activeDaoNominations += 1;
        emit newDaoNomination(newDAO, _msgSender());
    }

    function closeNewDAOVoting(address newDAO) external {
        require(block.timestamp > (_newDAONominations[newDAO].timeOfNomination + daoVotingDuration), "We have not passed the minimum voting duration");
        require(!_newDAONominations[newDAO].votingClosed, "Voting has already closed for this nomination");
        require(approvedNewDAO == address(0), "There is already an approved new DAO");

        if(_newDAONominations[newDAO].votesFor > _newDAONominations[newDAO].votesAgainst){
            approvedNewDAO = newDAO;
            daoApprovedTime = block.timestamp;
        }
        activeDaoNominations -= 1;
        _newDAONominations[newDAO].votingClosed = true;
    }

    function updateDAOAddress() external {
        require(approvedNewDAO != address(0),"There is not an approved new DAO");
        require(block.timestamp > (daoApprovedTime + daoUpdateDelay), "We have not finished the delay for an approved DAO");
        apolloToken.changeArtistAddress(approvedNewDAO);
    }

    function reflectBalance(uint256 amountToReflect) external {
        require(apolloToken.artistDAO() != address(this), "This function cannot be called while this contract is the DAO");
        if(amountToReflect == 0){
            amountToReflect = apolloToken.balanceOf(address(this));
        }
        apolloToken.reflect(amountToReflect);
    }
}