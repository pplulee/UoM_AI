import java.util.ArrayList;

/**
 * @author Mbassip2
 */
public class BoardState {


    private final int[][] board;
    public int colour;


    public BoardState() {

        // Create board
        board = new int[8][8];
    }


    // Clone the current object
    public BoardState deepCopy() {

        BoardState newBoardState = new BoardState();
        for (int i = 0; i < 8; i++)
            for (int j = 0; j < 8; j++)
                newBoardState.setContents(i, j, getContents(i, j));
        newBoardState.colour = colour;
        return newBoardState;
    }


    public int getContents(int x, int y) {

        return board[x][y];
    }

    public void setContents(int x, int y, int piece) {

        board[x][y] = piece;
    }

    // Under construction Assumes coordinates are in order.


    private boolean checkOnBoard(int x, int y) {

        return (x >= 0) && (x < 8) && (y >= 0) && (y < 8);
    }


    // Returns the list of legal moves for current player.
    public ArrayList<Move> getLegalMoves() {

        // Very simple method
        ArrayList<Move> ans = new ArrayList<Move>();
        for (int i = 0; i < 8; i++)
            for (int j = 0; j < 8; j++)
                if (checkLegalMove(i, j))
                    ans.add(new Move(i, j));
        return ans;
    }


    // Tests whether the game is over
    public boolean gameOver() {

        boolean ans = false;
        if (getLegalMoves().isEmpty()) {
            colour = -colour;              // change colour temporarily
            if (getLegalMoves().isEmpty())
                ans = true;
            colour = -colour;               // change colour back
        }
        return ans;
    }


    public boolean checkLegalMove(int x, int y) {
        return
                checkOnBoard(x, y) && (getContents(x, y) == 0) &&
                        ((checkLeft(x, y) != -1) || (checkRight(x, y) != -1) ||
                                (checkUp(x, y) != -1) || (checkDown(x, y) != -1) ||
                                (checkUpLeft(x, y) != -1) || (checkUpRight(x, y) != -1) ||
                                (checkDownLeft(x, y) != -1) || (checkDownRight(x, y) != -1));
    }


    public void makeLegalMove(int x, int y) {

        int a, b; // work variables (indices)

        // Current square
        // setContents(x, y, colour);

        // Squares to left
        a = checkLeft(x, y);
        if (a != -1)
            for (int i = x; i > a; i--)
                setContents(i, y, colour);

        // Squares to right
        a = checkRight(x, y);
        if (a != -1)
            for (int i = x; i < a; i++)
                setContents(i, y, colour);


        // Squares above
        a = checkUp(x, y);
        if (a != -1)
            for (int j = y; j > a; j--)
                setContents(x, j, colour);


        // Squares below
        a = checkDown(x, y);
        if (a != -1)
            for (int j = y; j < a; j++)
                setContents(x, j, colour);


        // Squares to above left
        a = checkUpLeft(x, y);
        if (a != -1)
            for (int i = x, j = y; i > a; i--, j--)
                setContents(i, j, colour);

        // Squares above right
        a = checkUpRight(x, y);
        if (a != -1)
            for (int i = x, j = y; i < a; i++, j--)
                setContents(i, j, colour);


        // Squares to below left
        a = checkDownLeft(x, y);
        if (a != -1)
            for (int i = x, j = y; i > a; i--, j++)
                setContents(i, j, colour);

        // Squares below right
        a = checkDownRight(x, y);
        if (a != -1)
            for (int i = x, j = y; i < a; i++, j++)
                setContents(i, j, colour);
        colour = -colour;                         // Change player


        // Now the computer moves 

    }


    // Return largest value of i < x st board[j,i] is opposite to color for all
    // j (i < j < x) and board[i,y] is colour, and return -1 if none in range
    private int checkLeft(int x, int y) {

        int i = x - 1;
        while ((i > 0) && (getContents(i, y) == -colour))  //check almost to start
            i--;
        if ((i < x - 1) && getContents(i, y) == colour)
            return i;
        else
            return -1;
    }


    // Return largest value of i > x st board[j,i] is opposite to color for all
    // j (i > j > x) and board[i,y] is colour, and return -1 if none in range
    private int checkRight(int x, int y) {

        int i = x + 1;
        while ((i < 7) && (getContents(i, y) == -colour))   // Check almost to end
            i++;
        if ((i > x + 1) && getContents(i, y) == colour)
            return i;
        else
            return -1;
    }

    // Return largest value of i < y st board[x,j] is opposite to color for all
    // j (i < j < y) and board[x,i] is colour, and return -1 if none in range
    private int checkUp(int x, int y) {

        int i = y - 1;
        while ((i > 0) && (getContents(x, i) == -colour)) // Check almost to start
            i--;
        if ((i < y - 1) && getContents(x, i) == colour)
            return i;
        else
            return -1;
    }


    // Return largest value of i > y st board[x,j] is opposite to color for all
    // j (i > j > y) and board[x,i] is colour, and return -1 if none in range
    private int checkDown(int x, int y) {

        int i = y + 1;
        while ((i < 7) && (getContents(x, i) == -colour))   // Check almost to end
            i++;
        if ((i > y + 1) && getContents(x, i) == colour)
            return i;
        else
            return -1;
    }


    // Return largest value of i < x st board[x-j,y-j] is opposite to color for all
    // j (i < j < endOfBoard) and board[i,y] is colour, and return -1 if none in range
    private int checkUpLeft(int x, int y) {

        int i = x - 1;
        int j = y - 1;
        while ((i > 0) && (j > 0) && (getContents(i, j) == -colour)) {  //check almost to start
            i--;
            j--;
        }
        if ((i < x - 1) && getContents(i, j) == colour)
            return i;
        else
            return -1;
    }


    // Return largest value of i > x st board[j,i] is opposite to color for all
    // j (i > j > x) and board[i,y] is colour, and return -1 if none in range
    private int checkUpRight(int x, int y) {

        int i = x + 1;
        int j = y - 1;
        while ((i < 7) && (j > 0) && (getContents(i, j) == -colour)) {  // Check almost to end
            i++;
            j--;
        }
        if ((i > x + 1) && getContents(i, j) == colour)
            return i;
        else
            return -1;
    }


    // Return largest value of i < x st board[x-j,y-j] is opposite to color for all
    // j (i < j < endOfBoard) and board[i,y] is colour, and return -1 if none in range
    private int checkDownLeft(int x, int y) {

        int i = x - 1;
        int j = y + 1;
        while ((i > 0) && (j < 7) && (getContents(i, j) == -colour)) {  //check almost to start
            i--;
            j++;
        }
        if ((i < x - 1) && getContents(i, j) == colour)
            return i;
        else
            return -1;
    }


    // Return largest value of i > x st board[j,i] is opposite to color for all
    // j (i > j > x) and board[i,y] is colour, and return -1 if none in range
    private int checkDownRight(int x, int y) {

        int i = x + 1;
        int j = y + 1;
        while ((i < 7) && (j < 7) && (getContents(i, j) == -colour)) {  // Check almost to end
            i++;
            j++;
        }
        if ((i > x + 1) && getContents(i, j) == colour)
            return i;
        else
            return -1;
    }


    public String resultString() {

        String ans;
        int[] score = totUp();
        int white = score[0];
        int black = score[1];
        if (white > black)
            ans = "White wins";
        else if (black > white)
            ans = "Black wins";
        else
            ans = "Draw";
        ans += "[White: " + white + "; black: " + black + "]";
        return ans;
    }

    public int[] totUp() {

        int[] ans = new int[2]; // white count then black count
        int white = 0;
        int black = 0;
        for (int i = 0; i < 8; i++)
            for (int j = 0; j < 8; j++)
                if (getContents(i, j) == 1)
                    white++;
                else if (getContents(i, j) == -1)
                    black++;
        ans[0] = white;
        ans[1] = black;
        return ans;
    }

    // Return result as integer: <0 black win; 0 draw; >0 white win
    public int result() {
        int[] scores = totUp();  // result vector for when game over
        return scores[0] - scores[1];
    }
}
