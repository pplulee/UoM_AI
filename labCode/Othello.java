/**
 * @author Mbassip2
 */
public class Othello {

    public static final int SQUARESIZE = 60;   // Basic dimensions of board
    public static final double PIECERATIO = 0.4; // ration of radius of piece to square size
    public static final int xBOARDpos = 100;   // Position of board
    public static final int yBOARDpos = 100;   // Position of board
    public static final int xMARGIN = 50;   // Position of board
    public static final int yMARGIN = 50;   // Position of board
    public static final int searchDepth = 6;   // Depth of minimax search


    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        BoardState initialState = new BoardState();
        initialState.setContents(3, 3, 1);
        initialState.setContents(3, 4, -1);
        initialState.setContents(4, 3, -1);
        initialState.setContents(4, 4, 1);
        initialState.colour = -1;              // Black to start

        MoveChooser mc = new MoveChooser();

        OthelloDisplay othelloDisplay = new OthelloDisplay();
        othelloDisplay.boardState = initialState;
        othelloDisplay.repaint();
    }
}
