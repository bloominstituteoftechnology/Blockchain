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

	private let baseURL = URL(string: "http://localhost:5000")!

	func getLatestChain(completion: @escaping (ChainController) -> Void) {
		let url = baseURL.appendingPathComponent("chain")

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

	func sendMoney(from sender: String, to recipient: String, amount: Double, completion: @escaping (ChainController, NetworkError?) -> Void) {
		let url = baseURL
			.appendingPathComponent("transaction")
			.appendingPathComponent("new")

		let trans = Transaction(sender: sender, recipient: recipient, amount: amount, timestamp: Date().timeIntervalSince1970, id: "")

		let json = try! JSONEncoder().encode(trans)

		var request = url.request
		request.httpMethod = .post
		request.httpBody = json
		request.addValue(.contentType(type: .json), forHTTPHeaderField: .commonKey(key: .contentType))

		handler.transferMahCodableDatas(with: request) { (result: Result<Message, NetworkError>) -> Void in
			switch result {
			case .success:
				completion(self, nil)
			case .failure(let error):
				completion(self, error)
				switch error {
				case .httpNon200StatusCode(code: let code, data: let data):
					print(code)
					let str = String(data: data!, encoding: .utf8)!
					print(str)
				default:
					break
				}
			}
		}
	}

	func transactions(for user: String) -> [Transaction] {
		chain.flatMap { $0.transactions }.filter { $0.sender == user || $0.recipient == user }
	}

	func balance(for user: String, transactions: [Transaction]) -> (balance: Double, sent: Double, received: Double) {
		var balance = 0.0
		var totalSent = 0.0
		var totalReceived = 0.0

		for transaction in transactions {
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

struct Transaction: Codable, Hashable, CustomStringConvertible {
	let sender: String
	let recipient: String
	let amount: Double
	let timestamp: Double
	let id: String

	var description: String {
		"\(sender) sent \(amount) coins to \(recipient) at \(timestamp)"
	}
}

struct Message: Codable {
	let message: String
}
