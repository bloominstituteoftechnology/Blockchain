//
//  ContentView.swift
//  BCWallet
//
//  Created by Michael Redig on 2/13/20.
//  Copyright © 2020 Red_Egg Productions. All rights reserved.
//

import SwiftUI

struct ContentView: View {

	@State private var data = ["a", "b", "c"]

	@State private var userID = ""
	@State private var totalSent: CGFloat = 0
	@State private var totalReceived: CGFloat = 0
	@State private var currentBalance: CGFloat = 0

    var body: some View {
		Form {
			Section(header: Text("Sign In:")) {
				HStack(alignment: .center) {
					Text("Enter your ID: ")
					TextField("mahname", text: $userID)
						.textFieldStyle(RoundedBorderTextFieldStyle())
					Button(action: {
						switch Int.random(in: 0...4) {
						case 0:
							self.currentBalance += 10
						case 1:
							self.currentBalance -= 10.5
						case 2:
							self.totalReceived += 5
						case 3:
							self.totalSent += 6.4
						case 4:
							let alpha  = Array("abcdefghijklmnopqrstuvwxyz").compactMap { String($0) }
							self.data.append(alpha.randomElement() ?? "wrong")
						default:
							print("defaulted?")
						}
					}) {
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
					Text(datum)
				}
			}
		}
	}
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
