import java.util.ArrayList;

public class MoveChooser {

    public static Move chooseMove(BoardState boardState) {
        int searchDepth = Othello.searchDepth;

        ArrayList<Move> moves = boardState.getLegalMoves();
        if (moves.isEmpty()) {
            return null;
        }
        if (moves.size()== 1) {
            return moves.get(0);
        }
        int bestMove = 0;
        int bestScore = -1000;
        for (int i = 0; i < moves.size(); i++) {
            BoardState tmpBoard = boardState.deepCopy();
            tmpBoard.makeLegalMove(moves.get(i).x, moves.get(i).y);
            int tmpScore = minMax(tmpBoard, searchDepth - 1, -1000, 1000);
            if (tmpScore > bestScore) {
                bestMove = i;
            }
        }
        System.out.println("Choose "+bestMove+" in "+moves.size());
        return moves.get(bestMove);
    }

    public static int getWeight(BoardState tmpBoard, int Color){
        int[][] WeightTable = new int[][]{
                {120, -20, 20, 5, 5, 20, -20, 120},
                {-20, -40, -5, -5, -5, -5, -40, -20},
                {20, -5, 15, 3, 3, 15, -5, 20},
                {5, -5, 3, 3, 3, 3, -5, 5},
                {5, -5, 3, 3, 3, 3, -5, 5},
                {20, -5, 15, 3, 3, 15, -5, 20},
                {-20, -40, -5, -5, -5, -5, -40, -20},
                {120, -20, 20, 5, 5, 20, -20, 120}
        };
        int score = 0;
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                if (tmpBoard.getContents(i,j)!=0){
                    if (tmpBoard.getContents(i,j)==Color){
                        score += WeightTable[i][j];
                    }else{
                        score -= WeightTable[i][j];
                    }
                }
            }
        }
        return score;
    }
    public static int minMax(BoardState tmpBoard, int deepth, int alpha, int beta) {
        System.out.println("Deepth: "+deepth+" alpha: "+alpha+" beta: "+beta);
        if (deepth==0){
            return getWeight(tmpBoard, tmpBoard.colour);
        }
        ArrayList<Move> moves = tmpBoard.getLegalMoves();
        if (moves.isEmpty()) {
            return getWeight(tmpBoard, tmpBoard.colour);
        }
        for (int i=0;i<moves.size();i++){
            BoardState tmpBoard2 = tmpBoard.deepCopy();
            tmpBoard2.makeLegalMove(moves.get(i).x,moves.get(i).y);
            int currentScore = minMax(tmpBoard2,deepth-1,alpha,beta);
        }
    }
}
