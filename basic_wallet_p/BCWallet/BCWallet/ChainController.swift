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
		var balance = 0.0
		var totalSent = 0.0
		var totalReceived = 0.0

		let xtions = chain.flatMap { $0.transactions }.filter { $0.sender == user || $0.recipient == user }

		for transaction in xtions {
			if transaction.sender == user {
				balance -= transaction.amount
				totalSent += transaction.amount
			}
			if transaction.recipient == user {
				balance += transaction.amount
				totalReceived += transaction.amount
			}
		}

		return (balance, totalSent, totalReceived)
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
