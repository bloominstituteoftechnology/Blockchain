//
//  ContentView.swift
//  BCWallet
//
//  Created by Michael Redig on 2/13/20.
//  Copyright © 2020 Red_Egg Productions. All rights reserved.
//

import SwiftUI
import NetworkHandler

struct ContentView: View {

	private let controller = ChainController()

	@State private var data = [Transaction]()

	@State private var userID = ""
	@State private var totalSent = 0.0
	@State private var totalReceived = 0.0
	@State private var currentBalance = 0.0

    var body: some View {
		Form {
			Section(header: Text("Sign In:")) {
				HStack(alignment: .center) {
					Text("Enter your ID: ")
					TextField("mahname", text: $userID)
						.textFieldStyle(RoundedBorderTextFieldStyle())
					Button(action: fetchBalance) {
						Text("Submit")
					}
				}
				.frame(maxWidth: .infinity)
			}

			Section(header: Text("Current Balance")) {
				Text("\(currentBalance) coins")
			}
			Section(header: Text("Total Sent")) {
				Text("\(totalSent) coins")
			}
			Section(header: Text("Total Received")) {
				Text("\(totalReceived) coins")
			}

			Section(header: Text("Data")) {
				List(data, id: \.self) { datum in
					Text("\(datum.description)")
				}
			}
		}
	}

	func fetchBalance() {
		controller.getLatestChain { controller in
			let transactions = controller.transactions(for: self.userID)
			self.data = transactions

			let balanceInfo = controller.balance(for: self.userID, transactions: transactions)
			self.currentBalance = balanceInfo.balance
			self.totalSent = balanceInfo.sent
			self.totalReceived = balanceInfo.received
		}
	}
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
