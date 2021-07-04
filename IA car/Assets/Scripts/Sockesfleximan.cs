using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Net.Sockets;
//using System.Globalization.NumberStyles;

public class Sockesfleximan : MonoBehaviour {
	public string tekst;

	public float rotatieX;

	public float rotatieY;

	public float rotatieZ;

	public Transform nek;





	public byte[] bytesX = new byte[4];

	public byte[] bytesY = new byte[4];

	public byte[] bytesZ = new byte[4];

	public byte[] bytesW = new byte[4];



	public float xValue= (float)0.0;

	public float yValue= (float)0.0;

	public float zValue= (float)0.0;





	public Quaternion rot=Quaternion.identity;

	public Quaternion sensor=Quaternion.identity;





	public float[] qq = new float[4];



	internal bool socketReady = false;

	TcpClient mySocket;

	NetworkStream theStream;

	StreamWriter theWriter;

	StreamReader theReader;

	string Host = "localhost";

	int Port = 5333;



	void Update()

	{

		string receivedText = readSocket();

		if (receivedText != "")

		{

			tekst=receivedText;



			bytesX[0]=(byte)(HexToByte(tekst.Substring(0,1))*16+HexToByte(tekst.Substring(1,1)));

			bytesX[1]=(byte)(HexToByte(tekst.Substring(2,1))*16+HexToByte(tekst.Substring(3,1)));

			bytesX[2]=(byte)(HexToByte(tekst.Substring(4,1))*16+HexToByte(tekst.Substring(5,1)));

			bytesX[3]=(byte)(HexToByte(tekst.Substring(6,1))*16+HexToByte(tekst.Substring(7,1)));

			bytesY[0]=(byte)(HexToByte(tekst.Substring(8,1))*16+HexToByte(tekst.Substring(9,1)));

			bytesY[1]=(byte)(HexToByte(tekst.Substring(10,1))*16+HexToByte(tekst.Substring(11,1)));

			bytesY[2]=(byte)(HexToByte(tekst.Substring(12,1))*16+HexToByte(tekst.Substring(13,1)));

			bytesY[3]=(byte)(HexToByte(tekst.Substring(14,1))*16+HexToByte(tekst.Substring(15,1)));

			bytesZ[0]=(byte)(HexToByte(tekst.Substring(16,1))*16+HexToByte(tekst.Substring(17,1)));

			bytesZ[1]=(byte)(HexToByte(tekst.Substring(18,1))*16+HexToByte(tekst.Substring(19,1)));

			bytesZ[2]=(byte)(HexToByte(tekst.Substring(20,1))*16+HexToByte(tekst.Substring(21,1)));

			bytesZ[3]=(byte)(HexToByte(tekst.Substring(22,1))*16+HexToByte(tekst.Substring(23,1)));

			bytesW[0]=(byte)(HexToByte(tekst.Substring(24,1))*16+HexToByte(tekst.Substring(25,1)));

			bytesW[1]=(byte)(HexToByte(tekst.Substring(26,1))*16+HexToByte(tekst.Substring(27,1)));

			bytesW[2]=(byte)(HexToByte(tekst.Substring(28,1))*16+HexToByte(tekst.Substring(29,1)));

			bytesW[3]=(byte)(HexToByte(tekst.Substring(30,1))*16+HexToByte(tekst.Substring(31,1)));



			sensor.x=System.BitConverter.ToSingle( bytesX, 0); 

			sensor.y=System.BitConverter.ToSingle( bytesY, 0); 

			sensor.z=System.BitConverter.ToSingle( bytesZ, 0); 

			sensor.w=System.BitConverter.ToSingle( bytesW, 0); 



			qq[0]=System.BitConverter.ToSingle( bytesX, 0);

			qq[1]=System.BitConverter.ToSingle( bytesY, 0);

			qq[2]=System.BitConverter.ToSingle( bytesZ, 0);

			qq[3]=System.BitConverter.ToSingle( bytesW, 0);



			rotatieX=sensor.eulerAngles.x;

			rotatieY=sensor.eulerAngles.y;

			rotatieZ=sensor.eulerAngles.z;







			//      rot.x=sensor.x;

			//      rot.y=sensor.y;

			//      rot.z=sensor.z;

			//      rot.w=sensor.w;



			rot.x=-qq[1];

			rot.y=qq[0];

			rot.z=-qq[2];

			rot.w=qq[3];



			rot *= Quaternion.Euler(Vector3.up * yValue);

			rot *= Quaternion.Euler(Vector3.right * xValue);

			rot *= Quaternion.Euler(Vector3.forward * zValue);







			//rot *= Quaternion.Euler(Vector3(90,90,90));





			nek.rotation=rot;

			//nek.rotation=Quaternion.Euler(-rotatieY,rotatieX,-rotatieZ);

		}

	}



	void OnGUI()

	{



		if (!socketReady)

		{  

			if (GUILayout.Button("Connect"))

			{

				setupSocket();

				writeSocket("serverStatus:");

			}

		}



		// if (GUILayout.Button("Send"))

		// {

		//     writeSocket("test string");

		// }



		// if (GUILayout.Button("Close"))

		// {

		//     closeSocket();

		// }



		//GUI.Label(new Rect(0, 40, 1000, 400), tekst);

		if (socketReady)

		{  

			xValue = GUI.HorizontalSlider (new Rect (25, 25, 360, 30), (float)xValue, 180.0f, -180.0f);

			yValue = GUI.HorizontalSlider (new Rect (25, 50, 360, 30), (float)yValue, 180.0f, -180.0f);

			zValue = GUI.HorizontalSlider (new Rect (25, 75, 360, 30), (float)zValue, 180.0f, -180.0f);

		}



	}



	void OnApplicationQuit()

	{

		closeSocket();

	}



	public void setupSocket()

	{

		try

		{

			mySocket = new TcpClient(Host, Port);

			theStream = mySocket.GetStream();

			theWriter = new StreamWriter(theStream);

			theReader = new StreamReader(theStream);

			socketReady = true;

		}



		catch(Exception e)

		{

			Debug.Log("Socket error: " + e);

		}

	}



	public void writeSocket(string theLine)

	{

		if (!socketReady)

			return;

		string foo = theLine + "\r\n";

		theWriter.Write(foo);

		theWriter.Flush();

	}



	public string readSocket()

	{

		if (!socketReady)

			return "";

		if (theStream.DataAvailable)

			return theReader.ReadLine();

		//return theReader.ReadToEnd();

		return "";

	}



	public void closeSocket()

	{

		if (!socketReady)

			return;

		theWriter.Close();

		theReader.Close();

		mySocket.Close();

		socketReady = false;

	}



	private byte HexToByte(string hexVal)

	{

		if (hexVal=="0") return (0);

		else if (hexVal=="1") return (1);

		else if (hexVal=="2") return (2);

		else if (hexVal=="3") return (3);

		else if (hexVal=="4") return (4);

		else if (hexVal=="5") return (5);

		else if (hexVal=="6") return (6);

		else if (hexVal=="7") return (7);

		else if (hexVal=="8") return (8);

		else if (hexVal=="9") return (9);

		else if (hexVal=="A") return (10);

		else if (hexVal=="B") return (11);

		else if (hexVal=="C") return (12);

		else if (hexVal=="D") return (13);

		else if (hexVal=="E") return (14);

		else if (hexVal=="F") return (15);

		else return (0);

	}

}
