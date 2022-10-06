import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

/**
 * @author Mbassip2
 */
public class OthelloDisplay extends JFrame implements MouseListener {

    public BoardState boardState;
    public int colour;

    int xBoardstart;
    int yBoardstart;

    String resultString;

    private static final int xMargin = Othello.xMARGIN;
    private static final int yMargin = Othello.yMARGIN;

    private static final int winXSize = 8 * Othello.SQUARESIZE + 2 * xMargin;
    private static final int winYSize = 8 * Othello.SQUARESIZE + 3 * yMargin;
    private final Color mainColour = Color.green;

    public OthelloDisplay() {

        xBoardstart = xMargin;
        yBoardstart = 2 * yMargin;
        resultString = "";

        setTitle("emag isrever s'HP naI");

        setSize(winXSize, winYSize);
        setLocation(Othello.xBOARDpos, Othello.yBOARDpos);
        getContentPane().setBackground(mainColour);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        addMouseListener(this);
    }


    public void paint(Graphics g) {
        super.paint(g);

        // Draw the grid
        int x, y, s, r;  // work variables for coordinates
        x = xBoardstart;
        y = yBoardstart;
        r = (int) (Othello.SQUARESIZE * Othello.PIECERATIO);
        for (int i = 0; i < 9; i++) {
            g.drawLine(x, yBoardstart, x, yBoardstart + 8 * Othello.SQUARESIZE - 1);
            x += Othello.SQUARESIZE;
            g.drawLine(xBoardstart, y, xBoardstart + 8 * Othello.SQUARESIZE - 1, y);
            y += Othello.SQUARESIZE;
        }

        g.drawString("Ian Pratt-Hartmann 2020",
                xBoardstart + 8 * Othello.SQUARESIZE - 100, yBoardstart + 8 * Othello.SQUARESIZE + 25);
        g.drawString(resultString, 20, 70);
        // Draw the pieces
        for (int i = 0; i < 8; i++)
            for (int j = 0; j < 8; j++) {
                x = xBoardstart + i * Othello.SQUARESIZE + Othello.SQUARESIZE / 2;
                y = yBoardstart + j * Othello.SQUARESIZE + Othello.SQUARESIZE / 2;
                if (boardState.getContents(i, j) == 1) {
                    g.setColor(Color.WHITE);
                    g.fillOval(x - r, y - r, 2 * r, 2 * r);
                } else if (boardState.getContents(i, j) == -1) {
                    g.setColor(Color.BLACK);
                    g.fillOval(x - r, y - r, 2 * r, 2 * r);
                }
            }
    }


    public void flashOpponentMove(int i, int j) {

        Graphics g = getGraphics();
        int x = xBoardstart + i * Othello.SQUARESIZE + Othello.SQUARESIZE / 2;
        int y = yBoardstart + j * Othello.SQUARESIZE + Othello.SQUARESIZE / 2;
        int r = (int) (Othello.SQUARESIZE * Othello.PIECERATIO);

        for (int h = 0; h < 10; h++) {
            if (boardState.colour == 1)
                g.setColor(Color.BLACK);
            else
                g.setColor(Color.WHITE);
            g.fillOval(x - r, y - r, 2 * r, 2 * r);
            paint(getGraphics());
            myWait(10000);
            g.setColor(Color.GREEN);
            g.fillOval(x - r, y - r, 2 * r, 2 * r);
            paint(getGraphics());
            myWait(10000);
        }
    }

    public void mouseClicked(MouseEvent e) {

    }

    @Override
    public void mousePressed(MouseEvent e) {

        // Assemble the action to be performed
        int i = xCanvasToSquare(e.getX());
        int j = yCanvasToSquare(e.getY());

        /*
        // 2-player (human-human) version
        
        if(boardState.getLegalMoves().isEmpty())   // User has no legal moves
            boardState.colour*= -1;                 // Reverse player
        else if(boardState.checkLegalMove(i,j)){
            boardState.makeLegalMove(i, j);
            paint(getGraphics());
            
        }
        */

        // 1-player (human-computer) version
        if (boardState.getLegalMoves().isEmpty()) {   // User has no legal moves
            boardState.colour *= -1;                 // Reverse player

            Move move = MoveChooser.chooseMove(boardState);
            if (move != null) {
                flashOpponentMove(move.x, move.y);
                boardState.makeLegalMove(move.x, move.y);
                paint(getGraphics());
            } else { // Computer has no moves either game over
                resultString = "Game over: " + boardState.resultString();
                paint(getGraphics());
            }
        } else if (boardState.checkLegalMove(i, j)) {
            boardState.makeLegalMove(i, j);
            paint(getGraphics());
            Move move = MoveChooser.chooseMove(boardState);
            if (move != null) {
                flashOpponentMove(move.x, move.y);
                boardState.makeLegalMove(move.x, move.y);
                paint(getGraphics());
            } else {   // Coomputer cannot move, so change back colour
                boardState.colour *= -1;
                if (boardState.getLegalMoves().isEmpty()) {  // Computer has no moves either game over
                    resultString = "Game over: " + boardState.resultString();
                    paint(getGraphics());
                }
            }
        }
        // Illegal move
        else {
            Toolkit.getDefaultToolkit().beep();
        }

    }

    @Override
    public void mouseReleased(MouseEvent e) {
    }

    @Override
    public void mouseEntered(MouseEvent e) {
    }

    @Override
    public void mouseExited(MouseEvent e) {
    }

    private int xCanvasToSquare(int x) {

        if ((x < xBoardstart) || (x > xBoardstart + 8 * Othello.SQUARESIZE))
            return -1;

        return (x - xBoardstart) / Othello.SQUARESIZE;
    }

    private int yCanvasToSquare(int y) {

        if ((y < yBoardstart) || (y > yBoardstart + 8 * Othello.SQUARESIZE))
            return -1;
        return (y - yBoardstart) / Othello.SQUARESIZE;
    }


    private void myWait(int x) {
        double w;
        for (int h = 0; h < 10 * x; h++)
            w = Math.sin(h);
    }

}
