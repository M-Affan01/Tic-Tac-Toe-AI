import streamlit as st
import time

# -----------------------------------------------------------------------------
# Configuration & CSS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Ultimate Tic Tac Toe AI", page_icon="🎮", layout="centered")

def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

        /* Modern Dark Theme & Background */
        .stApp {
            background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }

        /* Hide Streamlit Elements */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Glassmorphism Global Container */
        .main-container {
            max-width: 600px; /* Increased Max Width */
            margin: 0 auto;
            padding: 20px;
        }

        /* Title Styling */
        .title-text {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(to right, #00f260, #0575e6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 5px;
            text-shadow: 0 0 30px rgba(5, 117, 230, 0.6);
            letter-spacing: 3px;
        }
        
        .subtitle-text {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.6);
            text-align: center;
            margin-bottom: 25px;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        /* Scoreboard */
        .scoreboard {
            display: flex;
            justify-content: space-around;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 25px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
        }
        .score-item {
            text-align: center;
        }
        .score-label {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.6);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .score-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
        }
        
        /* Status Message Card */
        .status-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        
        .status-text {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: 1px;
            font-family: 'Orbitron', sans-serif;
        }

        /* Game Grid Container */
        .game-grid {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
            margin-bottom: 25px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* -----------------------------------------------------------
           Button Styling - Separating Grid (Secondary) vs Restart (Primary)
           ----------------------------------------------------------- */
           
        /* GRID BUTTONS (Secondary) */
        /* Target buttons that are NOT primary (Streamlit default is secondary) */
        div.stButton > button[kind="secondary"] {
            width: 100%;
            height: auto;
            aspect-ratio: 1 / 1; /* FORCE SQUARE */
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            font-size: 3rem;
            font-family: 'Orbitron', sans-serif; 
            font-weight: 900;
            color: rgba(255,255,255,0.1);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            justify-content: center;
            padding: 0;
            line-height: 0;
            margin-bottom: 0px; 
            margin-left: auto;
            margin-right: auto;
        }

        div.stButton > button[kind="secondary"]:hover {
            transform: translateY(-4px) scale(1.02);
            background: rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            border-color: rgba(255, 255, 255, 0.3);
            z-index: 2;
        }

        div.stButton > button[kind="secondary"]:active {
            transform: translateY(0) scale(0.98);
        }

        /* RESTART BUTTON (Primary) */
        div.stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.2rem;
            font-weight: 700;
            border-radius: 50px;
            margin-top: 15px;
            width: 100%;
            height: auto;
            aspect-ratio: auto !important; /* RESET ASPECT RATIO */
            letter-spacing: 2px;
            text-transform: uppercase;
            box-shadow: 0 4px 15px rgba(221, 36, 118, 0.5);
        }
        
        div.stButton > button[kind="primary"]:hover {
            box-shadow: 0 6px 20px rgba(221, 36, 118, 0.7);
            transform: translateY(-2px);
            filter: brightness(1.1);
        }
        
        /* Fallback for older Streamlit versions that don't output [kind] */
        /* We assume unclassified buttons are grid buttons mostly, but since we set type='primary' in python, it should work. */
        
        /* Grid Helpers */
        [data-testid="column"] {
            padding-left: 8px !important;
            padding-right: 8px !important;
        }
        
        /* Vertical & Horizontal Center Alignment Wrapper */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Footer */
        .footer {
            margin-top: 50px;
            text-align: center;
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.2);
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 2px;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# -----------------------------------------------------------------------------
# Game Logic
# -----------------------------------------------------------------------------

def initialize_game():
    if 'board' not in st.session_state:
        st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    if 'turn' not in st.session_state:
        st.session_state.turn = 'X'
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    
    # Score Tracking
    if 'scores' not in st.session_state:
        st.session_state.scores = {'X': 0, 'O': 0, 'Draw': 0}

def reset_game():
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    st.session_state.turn = 'X'
    st.session_state.winner = None
    st.session_state.game_over = False

def update_score(result):
    if result == 'X':
        st.session_state.scores['X'] += 1
    elif result == 'O':
        st.session_state.scores['O'] += 1
    else:
        st.session_state.scores['Draw'] += 1

def check_winner(board):
    lines = []
    # Rows
    for i in range(3): lines.append(board[i])
    # Cols
    for j in range(3): lines.append([board[0][j], board[1][j], board[2][j]])
    # Diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])
    
    for line in lines:
        if line[0] == line[1] == line[2] and line[0] != '':
            return line[0]
    return None

def is_board_full(board):
    return all(cell != '' for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'O': return 10 - depth
    if winner == 'X': return depth - 10
    if is_board_full(board): return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

def get_ai_move(board):
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

# -----------------------------------------------------------------------------
# UI Layout
# -----------------------------------------------------------------------------

initialize_game()

# Expanded Centered Layout [1, 3, 1] for wider board
_, main_col, _ = st.columns([1, 2.5, 1])

with main_col:
    # Title
    st.markdown('<div class="title-text">TIC TAC TOE</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">UNBEATABLE AI EDITION</div>', unsafe_allow_html=True)

    # Scoreboard
    st.markdown(f"""
        <div class="scoreboard">
            <div class="score-item">
                <div class="score-label">PLAYER (X)</div>
                <div class="score-value" style="color: #00f260;">{st.session_state.scores['X']}</div>
            </div>
            <div class="score-item">
                <div class="score-label">DRAWS</div>
                <div class="score-value" style="color: #00d2ff;">{st.session_state.scores['Draw']}</div>
            </div>
            <div class="score-item">
                <div class="score-label">AI (O)</div>
                <div class="score-value" style="color: #ff2a2a;">{st.session_state.scores['O']}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Status
    status_html = ""
    if st.session_state.game_over:
        if st.session_state.winner == 'X':
            status_html = '<div style="color: #00f260; text-shadow: 0 0 20px #00f260;">🎉 YOU WIN!</div>'
            st.balloons()
        elif st.session_state.winner == 'O':
            status_html = '<div style="color: #ff2a2a; text-shadow: 0 0 20px #ff2a2a;">🤖 AI WINS!</div>'
        else:
            status_html = '<div style="color: #00d2ff; text-shadow: 0 0 20px #00d2ff;">🤝 DRAW GAME</div>'
    else:
        if st.session_state.turn == 'X':
            status_html = '<div style="color: #fff;">YOUR TURN <span style="color:#00f260">(✕)</span></div>'
        else:
            status_html = '<div style="color: #fff; animation: pulse 1.5s infinite;">AI THINKING...</div>'

    st.markdown(f'<div class="status-card"><div class="status-text">{status_html}</div></div>', unsafe_allow_html=True)

    # Board
    for i in range(3):
        # Evenly spaced columns
        cols = st.columns(3, gap="small")
        for j in range(3):
            cell_value = st.session_state.board[i][j]
            
            # Custom Icons
            display_label = " "
            if cell_value == 'X':
                display_label = "✕" 
            elif cell_value == 'O':
                display_label = "◯"
            
            # Button
            btn = cols[j].button(
                display_label, 
                key=f"btn_{i}_{j}", 
                disabled=st.session_state.game_over or cell_value != '',
                use_container_width=True
            )
            
            # Logic
            if btn:
                if not st.session_state.game_over and st.session_state.turn == 'X':
                    st.session_state.board[i][j] = 'X'
                    
                    winner = check_winner(st.session_state.board)
                    if winner:
                        st.session_state.winner = winner
                        st.session_state.game_over = True
                        update_score(winner)
                    elif is_board_full(st.session_state.board):
                        st.session_state.game_over = True
                        update_score('Draw')
                    else:
                        st.session_state.turn = 'O'
                        st.rerun()
                    
                    if st.session_state.game_over:
                        st.rerun()

    # Restart
    if st.button("RESTART GAME", key="restart", help="Start a new game", type="primary", use_container_width=True):
        reset_game()
        st.rerun()
    
    # Footer
    st.markdown('<div class="footer">POWERED BY MINIMAX ALGORITHM • UNBEATABLE</div>', unsafe_allow_html=True)

    # Global CSS and JS Injection for High Visibility
    st.markdown("""
    <style>
    /* Ensure ALL buttons have visible text by default */
    div.stButton > button p {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        color: #ffffff !important; /* Bright White Default */
        mix-blend-mode: normal !important;
    }
    
    /* Specific Styling for X and O via Attribute Selectors if possible, 
       otherwise rely on JS injection below */
    </style>
    
    <script>
    // MutationObserver to watch for changes and apply styles dynamically
    const observer = new MutationObserver((mutations) => {
        const buttons = window.parent.document.querySelectorAll('button');
        buttons.forEach(btn => {
            // Check inner text for X or O
            if (btn.innerText.includes('✕')) {
                btn.style.color = '#00f260';
                btn.style.textShadow = '0 0 10px #00f260, 0 0 20px #00f260';
                btn.style.borderColor = 'rgba(0, 242, 96, 0.8)';
                btn.style.backgroundColor = 'rgba(0, 242, 96, 0.15)';
                btn.style.fontSize = '3.5rem';
                // Target inner p tag if exists
                const p = btn.querySelector('p');
                if (p) {
                    p.style.color = '#00f260';
                    p.style.textShadow = '0 0 10px #00f260';
                }
            } else if (btn.innerText.includes('◯')) {
                btn.style.color = '#ff2a2a';
                btn.style.textShadow = '0 0 10px #ff2a2a, 0 0 20px #ff2a2a';
                btn.style.borderColor = 'rgba(255, 42, 42, 0.8)';
                btn.style.backgroundColor = 'rgba(255, 42, 42, 0.15)';
                btn.style.fontSize = '3.5rem';
                // Target inner p tag if exists
                const p = btn.querySelector('p');
                if (p) {
                    p.style.color = '#ff2a2a';
                    p.style.textShadow = '0 0 10px #ff2a2a';
                }
            }
        });
    });
    
    // Start observing the document body for changes
    observer.observe(window.parent.document.body, { childList: true, subtree: true });
    
    // Initial run
    const buttons = window.parent.document.querySelectorAll('button');
    buttons.forEach(btn => {
        if (btn.innerText.includes('✕')) {
            btn.style.color = '#00f260';
            btn.style.textShadow = '0 0 10px #00f260';
        } else if (btn.innerText.includes('◯')) {
            btn.style.color = '#ff2a2a';
            btn.style.textShadow = '0 0 10px #ff2a2a';
        }
    });
    </script>
    """, unsafe_allow_html=True)

# AI Move
if st.session_state.turn == 'O' and not st.session_state.game_over:
    time.sleep(0.5)
    move = get_ai_move(st.session_state.board)
    if move:
        row, col = move
        st.session_state.board[row][col] = 'O'
        
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
            st.session_state.game_over = True
            update_score(winner)
        elif is_board_full(st.session_state.board):
            st.session_state.game_over = True
            update_score('Draw')
        else:
            st.session_state.turn = 'X'
        st.rerun()
