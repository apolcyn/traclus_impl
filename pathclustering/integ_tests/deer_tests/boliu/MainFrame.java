package boliu;
import javax.swing.*;
import java.awt.event.*;
import java.awt.*;
import java.util.*;

public class MainFrame extends JFrame { 

	private JPanel p = null;
	
	public MainFrame() {
		
	}
	public MainFrame(ArrayList<Trajectory> trajectoryAL, ArrayList<Cluster> clusterRepresentativeTrajectoryAL) {
	
		initWindow();
		showWindow();
		
		Graphics g = p.getGraphics();
		g.setColor(Color.GREEN);
		p.paint(g);
		drawTrajectory(trajectoryAL, clusterRepresentativeTrajectoryAL);

	}

	
	public void drawTrajectory(ArrayList<Trajectory> trajectoryAL, ArrayList<Cluster> clusterRepresentativeTrajectoryAL) {
		
		Graphics g = p.getGraphics();
		g.setColor(Color.GREEN);
		//LineObject obj;
		
		for(int i=0; i<trajectoryAL.size();i++) {
			for(int m=0; m<trajectoryAL.get(i).getM_pointArray().size()-2 ;m++) {
				int startX = (int)trajectoryAL.get(i).getM_pointArray().get(m).getM_coordinate(0);
				int startY = (int)trajectoryAL.get(i).getM_pointArray().get(m).getM_coordinate(1);
				int endX = (int)trajectoryAL.get(i).getM_pointArray().get(m+1).getM_coordinate(0);
				int endY = (int)trajectoryAL.get(i).getM_pointArray().get(m+1).getM_coordinate(1);
				
				g.drawLine(startX, startY, endX, endY);
			}
		}
		
		for(int i=0; i<clusterRepresentativeTrajectoryAL.size();i++) {
			for(int j=0; j<clusterRepresentativeTrajectoryAL.get(i).getM_PointArray().size()-2; j++) {
				int startX = (int)clusterRepresentativeTrajectoryAL.get(i).getM_PointArray().get(j).getM_coordinate(0);
				int startY = (int)clusterRepresentativeTrajectoryAL.get(i).getM_PointArray().get(j).getM_coordinate(1);
				int endX = (int)clusterRepresentativeTrajectoryAL.get(i).getM_PointArray().get(j+1).getM_coordinate(0);
				int endY = (int)clusterRepresentativeTrajectoryAL.get(i).getM_PointArray().get(j+1).getM_coordinate(1);
				
				g.setColor(Color.RED);
				g.drawLine(startX, startY, endX, endY);
			}
		}
		
	
	}
	
	public void initWindow() {
		if(null == p) {
		   p = new JPanel();
		}    
	}
	
	public void showWindow() {
		
		this.setBounds(200, 200, 1200, 900);
		this.setContentPane(p);
		this.setTitle("TraClusAlgorithm ---- By Bo Liu");
		this.setVisible(true);
		this.setResizable(true);
		this.addWindowListener(new WindowAdapter() {
		   public void windowClosing(WindowEvent e) {
		    System.exit(0);
		   }});
		
		
	}
}
	