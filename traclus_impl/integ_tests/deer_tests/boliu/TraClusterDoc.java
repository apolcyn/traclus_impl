package boliu;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Scanner;

public class TraClusterDoc {
	
	public int m_nDimensions;
	public int m_nTrajectories;
	public int m_nClusters;
	public double m_clusterRatio;
	public int m_maxNPoints;
	public ArrayList<Trajectory> m_trajectoryList;
	public ArrayList<Cluster> m_clusterList;
	
	public TraClusterDoc() {
			
		m_nTrajectories = 0;
		m_nClusters = 0;
		m_clusterRatio = 0.0;	
		m_trajectoryList = new ArrayList<Trajectory>();
		m_clusterList = new ArrayList<Cluster>();
	}
	
	public class Parameter {
		double epsParam;
		int minLnsParam;
	}
	
	boolean onOpenDocument(String inputFileName) {
		
		int nDimensions = 2;		// default dimension = 2
		int nTrajectories = 0;
		int nTotalPoints = 0;		//no use
		int trajectoryId;
		int nPoints;
		double value;
		

		DataInputStream in;
		BufferedReader inBuffer = null;
		try {
			in = new DataInputStream(new BufferedInputStream(   
			        new FileInputStream(inputFileName)));
			
			
			
			inBuffer = new BufferedReader(   
	                new InputStreamReader(in));
			
			
			nDimensions = Integer.parseInt(inBuffer.readLine());			// the number of dimensions
			m_nDimensions = nDimensions;
			nTrajectories = Integer.parseInt(inBuffer.readLine());		// the number of trajectories
			m_nTrajectories = nTrajectories;
			
			m_maxNPoints = -1;		// initialize for comparison
			
			// the trajectory Id, the number of points, the coordinate of a point ...
			for(int i=0; i<nTrajectories; i++) {				
	
				String str = inBuffer.readLine();
				
				Scanner sc = new Scanner(str); 
				
				trajectoryId = sc.nextInt();		//trajectoryID
				nPoints = sc.nextInt();				//nubmer of points in the trajectory
				
				if(nPoints > m_maxNPoints) m_maxNPoints = nPoints;
				nTotalPoints += nPoints;
				
				Trajectory pTrajectoryItem = new Trajectory(trajectoryId, nDimensions);
				
				
				for(int j=0; j<nPoints; j++) {
					
					CMDPoint point = new CMDPoint(nDimensions);   // initialize the CMDPoint class for each point
					
					for(int k =0; k< nDimensions; k++) {						
						value = sc.nextDouble();
						point.setM_coordinate(k, value);						
					}
					
					pTrajectoryItem.addPointToArray(point);				
				}
				
				m_trajectoryList.add(pTrajectoryItem);
				
//				for(int m=0; m<pTrajectoryItem.getM_pointArray().size();m++) {
//					System.out.print(pTrajectoryItem.getM_pointArray().get(m).getM_coordinate(0)+" ");
//				}
//				System.out.println();
				
			}			
			
//			System.out.println(m_nDimensions+"haha"+m_nTrajectories);
//			System.out.println(inBuffer.readLine());
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
			System.out.println("Unable to open input file");
		} catch (NumberFormatException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}  finally {
			try {
				inBuffer.close();
				
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
        		
		return true;
	}
	
	boolean onClusterGenerate(String clusterFileName, double epsParam, int minLnsParam) {
//////////////////////////////////////////////////still to be written
		
		ClusterGen generator = new ClusterGen(this);
		
		if(m_nTrajectories ==0) {
			System.out.println("Load a trajectory data set first");
		}
		
		// FIRST STEP: Trajectory Partitioning
		if (!generator.partitionTrajectory())
		{
			System.out.println("Unable to partition a trajectory\n");
			return false;
		}

		// SECOND STEP: Density-based Clustering
		if (!generator.performDBSCAN(epsParam, minLnsParam))
		{
			System.out.println("Unable to perform the DBSCAN algorithm\n");
			return false;
		}

		// THIRD STEP: Cluster Construction
		if (!generator.constructCluster())
		{
			System.out.println( "Unable to construct a cluster\n");
			return false;
		}

		
		for(int i=0; i<m_clusterList.size(); i++) {
			//m_clusterList.
			System.out.println(m_clusterList.get(i).getM_clusterId());
			for(int j=0; j<m_clusterList.get(i).getM_PointArray().size(); j++) {
				
				double x = m_clusterList.get(i).getM_PointArray().get(j).getM_coordinate(0);
				double y = m_clusterList.get(i).getM_PointArray().get(j).getM_coordinate(1);
			System.out.print("   "+ x +" "+ y +"   ");
			}
			System.out.println();
		}
		FileOutputStream fos = null;
		BufferedWriter bw = null;
		OutputStreamWriter osw = null;
		try {
			fos = new FileOutputStream(clusterFileName);
			osw = new OutputStreamWriter(fos);
			bw = new BufferedWriter(osw);
			
			bw.write("epsParam:"+epsParam +"   minLnsParam:"+minLnsParam);
			
			for(int i=0; i<m_clusterList.size(); i++) {
				//m_clusterList.
				//System.out.println(m_clusterList.get(i).getM_clusterId());
				bw.write("\nclusterID: "+ m_clusterList.get(i).getM_clusterId()+"  Points Number:  "+m_clusterList.get(i).getM_PointArray().size()+"\n");
				for(int j=0; j<m_clusterList.get(i).getM_PointArray().size(); j++) {
					
					double x = m_clusterList.get(i).getM_PointArray().get(j).getM_coordinate(0);
					double y = m_clusterList.get(i).getM_PointArray().get(j).getM_coordinate(1);
				//System.out.print("   "+ x +" "+ y +"   ");
					bw.write(x+" "+y+"   ");
				}
				//System.out.println();
			}						
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				bw.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
			
		}

		
		return true;		
	}

	
	
	Parameter onEstimateParameter()
	{
		Parameter p = new Parameter();
		
		ClusterGen generator = new ClusterGen(this);

		if (!generator.partitionTrajectory())
		{
			System.out.println("Unable to partition a trajectory\n");
			return null;
		}

		//if (!generator.estimateParameterValue(epsParam, minLnsParam))
		if (!generator.estimateParameterValue(p))
		{
			System.out.println("Unable to calculate the entropy\n");
			return null;
		}
		

		return p;
	}

	

}
