// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract EgoNFT is ERC721, Ownable {
    struct Ego {
        string image;
        string voice;
        address nftAddress;
        uint256 nftId;
    }

    mapping(uint256 => Ego) private _egos;

    constructor() ERC721("EgoNFT", "EGO") {}

    function mint(
        address to,
        uint256 tokenId,
        string memory image,
        string memory voice,
        address nftAddress,
        uint256 nftId
    ) public onlyOwner {
        // Check that 'to' is the owner of the external NFT
        require(
            IERC721(nftAddress).ownerOf(nftId) == to,
            "The address is not the owner of the external NFT"
        );
        _mint(to, tokenId);
        Ego memory newEgo = Ego(image, voice, nftAddress, nftId);
        _egos[tokenId] = newEgo;
    }

    function ego(uint256 tokenId) public view returns (Ego memory) {
        require(_exists(tokenId), "ERC721: queried token does not exist");
        return _egos[tokenId];
    }
}
