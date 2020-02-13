//
//  ChainController.swift
//  BCWallet
//
//  Created by Michael Redig on 2/13/20.
//  Copyright © 2020 Red_Egg Productions. All rights reserved.
//

import Foundation
import NetworkHandler

class ChainController {

	var chain: [Block] = []
	let handler = NetworkHandler()

	func getLatestChain(completion: @escaping (ChainController) -> Void) {
		let url = URL(string: "http://localhost:5000/chain")!

		handler.transferMahCodableDatas(with: url.request) { (result: Result<Chain, NetworkError>) -> Void in
			switch result {
			case .success(let chain):
				self.chain = chain.chain
			case .failure(let error):
				print("error fetching chain: \(error)")
			}
			completion(self)
		}
	}

	func balance(for user: String) -> (balance: Double, sent: Double, received: Double) {

		return (0,0,0)
	}
}

struct Chain: Codable {
	let chain: [Block]
	let length: Int
}

struct Block: Codable {
	let index: Int
	let previousHash: String
	let proof: Int
	let timestamp: Double
	let transactions: [Transaction]
}

struct Transaction: Codable {
	let sender: String
	let recipient: String
	let amount: Double
}
