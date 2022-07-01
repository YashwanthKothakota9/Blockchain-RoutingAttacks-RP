// SPDX-License-Identifier: MIT
pragma solidity ^0.4.11;

contract YAcoin_ico{
    //Introducing maximum number of YAcoins available for sale
    uint public max_yacoins=1000000;

    //USD to YAcoins conversion
    uint public usd_to_yacoins=1000;

    uint public total_yacoins_bought=0;

    mapping(address => uint) equity_yacoins;

    mapping(address => uint) equity_usd;

    //checking if an investor can buy YAcoins
    modifier can_buy_yacoins(uint usd_invested){
        require(usd_invested*usd_to_yacoins + total_yacoins_bought <= max_yacoins);
        _;
    }

    //Getting the equity in Yacoins of an investor
    function equity_in_yacoins(address investor) external constant returns(uint){
        return equity_yacoins[investor];
    }

    //Getting the equity in usd of an investor
    function equity_in_usd(address investor) external constant returns(uint){
        return equity_usd[investor];
    }

    //Buying YAcoins
    function buy_yacoins(address investor,uint usd_invested)external 
    can_buy_yacoins(usd_invested){
        uint yacoins_bought=usd_invested * usd_to_yacoins;
        equity_yacoins[investor] += yacoins_bought;
        equity_usd[investor] = equity_yacoins[investor] / 1000;
        total_yacoins_bought+=yacoins_bought;
    }

    //Selling YAcoins
    function sell_yacoins(address investor,uint yacoins_sold)external{
        equity_yacoins[investor] -= yacoins_sold;
        equity_usd[investor] = equity_yacoins[investor] / 1000;
        total_yacoins_bought -= yacoins_sold;
    }

}
