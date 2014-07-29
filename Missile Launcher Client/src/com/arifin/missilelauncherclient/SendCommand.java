/*
 * This class is the thread that sends networking commands to the 
 * Beaglebone server
 * 
 * Made by Stephen Arifin
 * 
 */

package com.arifin.missilelauncherclient;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.BlockingQueue;

public class SendCommand implements Runnable{

	// The Queue containing all the commands to be sent to the server
	private BlockingQueue<String> commandQueue;
	
	public SendCommand(BlockingQueue<String> commandQueue){
		this.commandQueue = commandQueue;
	}
	
	public void run() {
		
		while(true){
			try {
				// wait for a command to be added to the queue
				String command = commandQueue.take();
				
				// Open socket, send information, close socket
				Socket turretSocket = new Socket(Remote.SERVER_IP, Remote.SERVER_PORT);
				PrintWriter output = new PrintWriter(new BufferedWriter(
						new OutputStreamWriter(turretSocket.getOutputStream())), 
						true);
				output.println(command);
				turretSocket.close();
				
			} catch (UnknownHostException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			} catch (NullPointerException e){
				e.printStackTrace();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
}
