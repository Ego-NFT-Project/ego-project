// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract EgoNFT is ERC721, Ownable {
    struct Ego {
        string ego;
        address nftAddress;
        uint256 nftId;
    }

    mapping(uint256 => Ego) private _egos;

    constructor() ERC721("EgoNFT", "EGO") {}

    function mint(
        address to,
        uint256 tokenId,
        string memory _ego,
        address _nftAddress,
        uint256 _nftId
    ) public onlyOwner {
        // Check that 'to' is the owner of the external NFT
        require(
            IERC721(_nftAddress).ownerOf(_nftId) == to,
            "The address is not the owner of the external NFT"
        );
        _mint(to, tokenId);
        Ego memory newEgo = Ego(_ego, _nftAddress, _nftId);
        _egos[tokenId] = newEgo;
    }

    function ego(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "ERC721: queried token does not exist");
        Ego memory myEgo = _egos[tokenId];
        return myEgo.ego;
    }

    function nftAddress(uint256 tokenId) public view returns (address) {
        require(_exists(tokenId), "ERC721: queried token does not exist");
        Ego memory myEgo = _egos[tokenId];
        return myEgo.nftAddress;
    }

    function nftId(uint256 tokenId) public view returns (uint256) {
        require(_exists(tokenId), "ERC721: queried token does not exist");
        Ego memory myEgo = _egos[tokenId];
        return myEgo.nftId;
    }
}