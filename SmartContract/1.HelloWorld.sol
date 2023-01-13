pragma solidity >=0.4.22 <0.7.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */

contract Counter{
    uint public count = 10;
    
    event Increment(uint value);
    event Decrement(uint value);
    
    function getcount() view public returns(uint) {
        return count;    
    }
    
    function increament() public {
        count += 1;
        emit Increment(count);
    }
    
    function decrement() public {
        count -= 1;
        emit Decrement(count);
    }
}