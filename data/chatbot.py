import streamlit as st
import random
import pandas as pd
import os
import base64
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random 


class ChatBot:
    def __init__(self, course_data=None):
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        if 'past' not in st.session_state:
            st.session_state['past'] = []
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        if 'recommendations' not in st.session_state:
            st.session_state['recommendations'] = []
        if 'initial_message_shown' not in st.session_state:
            st.session_state['initial_message_shown'] = False
        if 'display_roadmap' not in st.session_state:
            st.session_state['display_roadmap']=False
        if 'current_roadmap' not in st.session_state:
            st.session_state['current_roadmap'] = None
        self.course_data = course_data
        
        # Initialize cosine similarity matrix if course data is available
        if self.course_data is not None:
            self.cosine_sim_mat = self.vectorize_text_to_cosine(self.course_data)

        self.topic_knowledge = self.load_topic_knowledge()

        self.roadmap_templates = self.load_roadmap_templates()
    
    def display_roadmap(self, roadmap):
        """Display the learning roadmap in an attractive format"""
        st.markdown(f"## 🗺️ {roadmap['title']}")
        st.markdown(f"*{roadmap['description']}*")
        
        # CSS for roadmap stages
        st.markdown("""
       <style>
.roadmap-stage {
    border-left: 4px solid #4CAF50; /* fixed to valid green color */
    padding: 10px 20px;
    margin-bottom: 15px;
    background-color: #ffffff; /* bright background for contrast */
    border-radius: 8px;
    position: relative;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.roadmap-stage:before {
    content: "";
    position: absolute;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background-color: #4CAF50;
    left: -10px;
    top: 16px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}

.stage-title {
    font-weight: bold;
    font-size: 1.2em;
    margin-bottom: 5px;
    color: #2E7D32;
}

.stage-duration {
    font-style: italic;
    color: #555;
    margin-bottom: 10px;
}

.skills-list {
    list-style-type: none;
    padding-left: 0;
}

.skills-list li {
    padding: 6px 0;
    position: relative;
    padding-left: 28px;
    font-size: 0.95em;
    color: #333;
}

.skills-list li:before {
    content: "✓";
    position: absolute;
    left: 0;
    top: 0;
    color: #4CAF50;
    font-weight: bold;
}
</style>
        """, unsafe_allow_html=True)
        
        for stage in roadmap['stages']:
            stage_html = f"""
            <div class="roadmap-stage">
                <div class="stage-title">{stage['title']}</div>
                <div class="stage-duration">Duration: {stage['duration']}</div>
                <ul class="skills-list">
            """
            
            for skill in stage['skills']:
                stage_html += f"<li>{skill}</li>"
                
            stage_html += """
                </ul>
            </div>
            """
            st.markdown(stage_html, unsafe_allow_html=True)
        
        # Add a prompt for courses
        st.markdown("### Ready to start learning?")
        st.markdown("Check out the recommended courses below to begin your learning journey!")
        
    def get_topic_explanation(self, subject):
        """Get explanation about a topic from knowledge base"""
        # Try direct match
        for topic, explanation in self.topic_knowledge.items():
            if subject.lower() == topic.lower():
                return explanation.strip()
        
        # Try partial match
        for topic, explanation in self.topic_knowledge.items():
            if subject.lower() in topic.lower() or topic.lower() in subject.lower():
                return explanation.strip()
        
        return None
        
    def get_roadmap(self, subject):
        """Get a learning roadmap for a specific subject"""
        # Try direct match
        for topic, roadmap in self.roadmap_templates.items():
            if subject.lower() == topic.lower():
                return roadmap
        
        # Try partial match
        for topic, roadmap in self.roadmap_templates.items():
            if subject.lower() in topic.lower() or topic.lower() in subject.lower():
                return roadmap
        
        return None



    def load_roadmap_templates(self):
        """Load learning roadmap templates from a JSON file"""
        # Example roadmap templates
        return {
            "python": {
                "title": "Python Learning Roadmap",
                "description": "A structured path to mastering Python programming.",
                "stages": [
                    {
                        "title": "Beginner",
                        "duration": "1 month",
                        "skills": ["Basic Syntax", "Data Types", "Control Flow"]
                    },
                    {
                        "title": "Intermediate",
                        "duration": "2 months",
                        "skills": ["Functions", "Modules", "File Handling"]
                    },
                    {
                        "title": "Advanced",
                        "duration": "3 months",
                        "skills": ["OOP", "Web Development", "Data Science"]
                    }
                ]
            },
            "web development": {
                "title": "Web Development Learning Roadmap",
                "description": "A comprehensive path to becoming a web developer, from fundamentals to advanced skills.",
                "stages": [
                    {
                        "title": "Stage 1: Web Fundamentals",
                        "duration": "4-6 weeks",
                        "skills": [
                            "HTML5 - Document structure, semantic elements, forms",
                            "CSS3 - Selectors, box model, layouts, responsive design",
                            "Basic JavaScript - Syntax, variables, data types, functions",
                            "Developer tools - Browser inspection, debugging"
                        ]
                    },
                    {
                        "title": "Stage 2: Frontend Development",
                        "duration": "8-12 weeks",
                        "skills": [
                            "Advanced JavaScript - DOM manipulation, events, AJAX",
                            "CSS frameworks (Bootstrap, Tailwind)",
                            "JavaScript frameworks basics (React, Vue, or Angular)",
                            "Version control with Git & GitHub"
                        ]
                    },
                    {
                        "title": "Stage 3: Backend Fundamentals",
                        "duration": "8-12 weeks",
                        "skills": [
                            "Server-side language (Node.js, Python, PHP, etc.)",
                            "RESTful API development",
                            "Database fundamentals (SQL and/or NoSQL)",
                            "Authentication & Authorization"
                        ]
                    },
                    {
                        "title": "Stage 4: Full-Stack Integration",
                        "duration": "8-12 weeks",
                        "skills": [
                            "Frontend-backend integration",
                            "State management",
                            "Full-stack project development",
                            "Deployment & hosting"
                        ]
                    },
                    {
                        "title": "Stage 5: Advanced Topics",
                        "duration": "Ongoing learning",
                        "skills": [
                            "Performance optimization",
                            "Progressive Web Apps (PWAs)",
                            "Testing (unit, integration, e2e)",
                            "CI/CD pipelines",
                            "Web security best practices"
                        ]
                    }
                ]
            },
             "business finance": {
                "title": "Business Finance Learning Roadmap",
                "description": "A comprehensive path to understanding business finance, from basics to advanced financial management.",
                "stages": [
                    {
                        "title": "Stage 1: Financial Fundamentals",
                        "duration": "4-6 weeks",
                        "skills": [
                            "Accounting basics - debits, credits, journal entries",
                            "Financial statements - balance sheet, income statement, cash flow",
                            "Time value of money concepts",
                            "Basic financial calculations and ratios"
                        ]
                    },
                    {
                        "title": "Stage 2: Financial Analysis",
                        "duration": "6-8 weeks",
                        "skills": [
                            "Financial statement analysis techniques",
                            "Profitability and efficiency ratios",
                            "Liquidity and solvency assessment",
                            "Industry benchmarking and comparison"
                        ]
                    },
                    {
                        "title": "Stage 3: Capital Management",
                        "duration": "6-8 weeks",
                        "skills": [
                            "Working capital management",
                            "Capital budgeting techniques (NPV, IRR, Payback)",
                            "Cost of capital calculation",
                            "Capital structure optimization"
                        ]
                    },
                    {
                        "title": "Stage 4: Risk Management and Valuation",
                        "duration": "6-8 weeks",
                        "skills": [
                            "Financial risk assessment",
                            "Hedging strategies and instruments",
                            "Business valuation methods",
                            "Mergers and acquisitions basics"
                        ]
                    },
                    {
                        "title": "Stage 5: Strategic Financial Management",
                        "duration": "Ongoing learning",
                        "skills": [
                            "Long-term financial planning",
                            "Dividend policy and share repurchases",
                            "International finance considerations",
                            "Financial technology integration",
                            "Ethical considerations in finance"
                        ]
                    }
                ]
            },
            "Guitar":{
                 "title": "Guitar Learning Roadmap",
                "description": "A structured path to mastering guitar playing.",
                "stages": [
                    {
                        "title": "Beginner",
                        "duration": "1 month",
                        "skills": ["Basic Chords", "Strumming Patterns", "Simple Songs"]
                    },
                    {
                        "title": "Intermediate",
                        "duration": "2 months",
                        "skills": ["Barre Chords", "Fingerstyle", "Music Theory Basics"]
                    },
                    {
                        "title": "Advanced",
                        "duration": "3 months",
                        "skills": ["Improvisation", "Advanced Techniques", "Songwriting"]
                    }
                ]
                
            },
            "Piano":{
                 "title": "Piano Learning Roadmap",
                "description": "A structured path to mastering piano playing.",
                "stages": [
                    {
                        "title": "Beginner",
                        "duration": "1 month",
                        "skills": ["Basic Notes", "Simple Melodies", "Hand Coordination"]
                    },
                    {
                        "title": "Intermediate",
                        "duration": "2 months",
                        "skills": ["Chords", "Scales", "Reading Sheet Music"]
                    },
                    {
                        "title": "Advanced",
                        "duration": "3 months",
                        "skills": ["Improvisation", "Complex Pieces", "Music Theory"]
                    }
                ]
                
            },
            "musical instruments": {
                "title": "Musical Instrument Learning Roadmap",
                "description": "A structured approach to learning any musical instrument, from basics to performance level.",
                "stages": [
                    {
                        "title": "Stage 1: Foundation",
                        "duration": "3-6 months",
                        "skills": [
                            "Instrument basics - parts, care, and maintenance",
                            "Proper posture and technique",
                            "Basic music theory - notation, rhythm, scales",
                            "Simple exercises and beginner pieces"
                        ]
                    },
                    {
                        "title": "Stage 2: Building Technical Skills",
                        "duration": "6-12 months",
                        "skills": [
                            "Regular practice routine development",
                            "Expanded technique exercises",
                            "Major and minor scales and arpeggios",
                            "Sight-reading practice",
                            "Introduction to different musical styles"
                        ]
                    },
                    {
                        "title": "Stage 3: Intermediate Development",
                        "duration": "1-2 years",
                        "skills": [
                            "Advanced techniques specific to your instrument",
                            "Music theory application - harmony, chord progressions",
                            "Repertoire expansion and interpretation",
                            "Ensemble playing or accompaniment",
                            "Performance preparation skills"
                        ]
                    },
                    {
                        "title": "Stage 4: Advanced Practice",
                        "duration": "2+ years",
                        "skills": [
                            "Complex technical exercises and etudes",
                            "Advanced repertoire and challenging pieces",
                            "Improvisation and creative expression",
                            "Performance experience and stage presence",
                            "Recording and self-evaluation techniques"
                        ]
                    },
                    {
                        "title": "Stage 5: Mastery and Specialization",
                        "duration": "Ongoing journey",
                        "skills": [
                            "Genre specialization or versatility",
                            "Personal style development",
                            "Advanced music theory and composition",
                            "Teaching abilities",
                            "Professional-level performances and collaborations"
                        ]
                    }
                ]
            },
             "programming": {
                "title": "Programming Learning Roadmap",
                "description": "A step-by-step guide to becoming proficient in programming, regardless of language choice.",
                "stages": [
                    {
                        "title": "Stage 1: Programming Fundamentals",
                        "duration": "4-8 weeks",
                        "skills": [
                            "Basic syntax and data types",
                            "Variables, constants, and operators",
                            "Control structures (conditionals, loops)",
                            "Functions and parameters",
                            "Basic input/output operations"
                        ]
                    },
                    {
                        "title": "Stage 2: Data Structures and Algorithms",
                        "duration": "8-12 weeks",
                        "skills": [
                            "Arrays, lists, stacks, and queues",
                            "Dictionaries/maps and sets",
                            "Basic searching and sorting algorithms",
                            "Recursion concepts",
                            "Time and space complexity basics"
                        ]
                    },
                    {
                        "title": "Stage 3: Object-Oriented Programming",
                        "duration": "6-10 weeks",
                        "skills": [
                            "Classes and objects",
                            "Inheritance and polymorphism",
                            "Encapsulation and abstraction",
                            "Interfaces and abstract classes",
                            "Design patterns introduction"
                        ]
                    },
                    {
                        "title": "Stage 4: Software Development Practices",
                        "duration": "8-12 weeks",
                        "skills": [
                            "Version control with Git",
                            "Testing methodologies",
                            "Debugging techniques",
                            "Code organization and documentation",
                            "Building complete applications"
                        ]
                    },
                    {
                        "title": "Stage 5: Specialization",
                        "duration": "Ongoing learning",
                        "skills": [
                            "Web development, mobile apps, data science, etc.",
                            "Advanced frameworks and libraries",
                            "Database integration",
                            "API development and consumption",
                            "Deployment and DevOps basics"
                        ]
                    }
                ]
            },
            "graphic design": {
                "title": "Graphic Design Learning Roadmap",
                "description": "A structured path to mastering graphic design skills.",
                "stages": [
                    {
                        "title": "Beginner",
                        "duration": "1 month",
                        "skills": ["Basic Design Principles", "Color Theory", "Typography"]
                    },
                    {
                        "title": "Intermediate",
                        "duration": "2 months",
                        "skills": ["Vector Graphics", "Layout Design", "Branding Basics"]
                    },
                    {
                        "title": "Advanced",
                        "duration": "3 months",
                        "skills": ["UI/UX Design", "Motion Graphics", "Portfolio Development"]
                    }
                ]
            },
             "digital marketing": {
                "title": "Digital Marketing Learning Roadmap",
                "description": "A comprehensive path to mastering digital marketing skills across various channels and strategies.",
                "stages": [
                    {
                        "title": "Stage 1: Digital Marketing Fundamentals",
                        "duration": "4-6 weeks",
                        "skills": [
                            "Digital marketing landscape and key channels",
                            "Marketing principles and consumer behavior",
                            "Basic analytics and metrics",
                            "Content creation fundamentals",
                            "Digital marketing tools overview"
                        ]
                    },
                    {
                        "title": "Stage 2: Content and SEO",
                        "duration": "6-8 weeks",
                        "skills": [
                            "Content strategy development",
                            "SEO fundamentals - on-page and off-page",
                            "Keyword research and optimization",
                            "Content creation for different platforms",
                            "Basic HTML and technical SEO"
                        ]
                    },
                    {
                        "title": "Stage 3: Social Media and Paid Advertising",
                        "duration": "6-8 weeks",
                        "skills": [
                            "Social media platform strategies",
                            "Community management and engagement",
                            "Paid social advertising campaigns",
                            "Google Ads and PPC fundamentals",
                            "Ad copywriting and creative development"
                        ]
                    },
                    {
                        "title": "Stage 4: Email, Analytics, and Conversion",
                        "duration": "6-8 weeks",
                        "skills": [
                            "Email marketing campaigns and automation",
                            "Google Analytics implementation and reporting",
                            "Conversion rate optimization techniques",
                            "A/B testing methodologies",
                            "Marketing funnels and user journey mapping"
                        ]
                    },
                    {
                        "title": "Stage 5: Advanced Digital Marketing",
                        "duration": "Ongoing learning",
                        "skills": [
                            "Integrated digital marketing strategies",
                            "Marketing automation",
                            "Advanced analytics and attribution modeling",
                            "Emerging platforms and technologies",
                            "Digital marketing leadership and team management"
                        ]
                    }
                ]
            }
        }

    def load_topic_knowledge(self):
        """Load topic knowledge about various topics"""
        return {
            "python": """
                Python is a high-level, interpreted programming language known for its readability and versatility.
                It supports multiple programming paradigms, including procedural, object-oriented, and functional programming.
                
                Key features of Python:
                
                - Easy to learn and use, making it ideal for beginners
                - Extensive standard library and third-party packages (e.g., NumPy, Pandas, Matplotlib)
                - Strong community support and documentation
                - Cross-platform compatibility (Windows, macOS, Linux)
                - Used in various fields such as web development, data science, machine learning, automation, and more
                
                Python's simplicity and power make it a popular choice for both novice and experienced developers.
            """,
            
            "web development": """
                Web development encompasses the creation and maintenance of websites and web applications.
                It involves a combination of programming, markup languages, design principles, and various tools.
                
                Web development is typically divided into:
                
                Frontend Development:
                - HTML for structure
                - CSS for styling and layout
                - JavaScript for interactivity
                - Frameworks like React, Angular, Vue
                
                Backend Development:
                - Server-side languages like Python, PHP, Ruby, Node.js
                - Databases (SQL or NoSQL)
                - APIs and web services
                - Server management
                
                Full-Stack Development combines both frontend and backend skills.
                
                Modern web development also encompasses responsive design, progressive web apps,
                accessibility considerations, performance optimization, and security best practices.
            """,

            "business finance": """
                Business Finance covers the principles, methods, and techniques for managing money and investments within organizations.
                It's essential for making informed financial decisions, planning for future growth, and ensuring the financial stability of a business.
                
                Key areas of Business Finance:
                
                - Financial Analysis: Interpreting financial statements and metrics to assess business performance
                - Capital Management: Optimizing the use of financial resources for daily operations and growth
                - Investment Appraisal: Evaluating potential investments using methods like NPV, IRR, and payback period
                - Risk Management: Identifying and mitigating financial risks through strategies like hedging
                - Financial Planning: Creating budgets, forecasts, and long-term financial strategies
                - Business Valuation: Determining the economic value of a business or its assets
                
                Understanding business finance is crucial for entrepreneurs, managers, and investors to make sound decisions
                that contribute to business growth and sustainability.
            """,

            "musical instruments": """
                Learning to play musical instruments offers both creative expression and cognitive benefits.
                Each instrument category has unique characteristics and learning approaches.
                
                Common categories of musical instruments:
                
                - String Instruments (Guitar, Violin, Cello, Bass):
                  Produce sound through vibrating strings, requiring finger dexterity and sometimes the use of bows or picks
                
                - Keyboard Instruments (Piano, Synthesizer, Organ):
                  Feature multiple keys that trigger sounds, excellent for understanding music theory and composition
                
                - Wind Instruments (Flute, Saxophone, Trumpet):
                  Generate sound through controlled airflow, developing breath control and embouchure skills
                
                - Percussion Instruments (Drums, Xylophone, Congas):
                  Create rhythm through striking or shaking, building timing and coordination
                
                Learning an instrument typically involves understanding music notation, developing technical skills,
                ear training, and regular practice. Many instruments can be learned at any age, though each presents
                unique physical and cognitive challenges.
            """,

            "programming": """
                Programming is the process of creating instructions that computers can understand and execute.
                It involves writing code in various programming languages to solve problems, automate tasks,
                and build software applications.
                
                Key concepts in programming:
                
                - Programming Languages: Formal languages with specific syntax and semantics (Python, Java, JavaScript, C++, etc.)
                - Data Structures: Methods of organizing and storing data (arrays, lists, dictionaries, etc.)
                - Algorithms: Step-by-step procedures for solving problems or performing tasks
                - Object-Oriented Programming: Paradigm focused on objects, classes, inheritance, and encapsulation
                - Functional Programming: Approach treating computation as the evaluation of mathematical functions
                - Testing and Debugging: Identifying and fixing errors in code
                
                Programming is a foundational skill for software development, data science, artificial intelligence,
                web development, game development, and many other technological fields.
            """,

            "digital marketing": """
                Digital Marketing involves promoting products, services, or brands using digital technologies
                and channels, primarily on the internet but also including mobile devices, display advertising,
                and other digital media.
                
                Key components of digital marketing:
                
                - Search Engine Optimization (SEO): Optimizing content to rank higher in search engine results
                - Content Marketing: Creating and distributing valuable content to attract and engage an audience
                - Social Media Marketing: Utilizing social platforms to connect with audiences and build brands
                - Email Marketing: Direct communication with prospects and customers via email campaigns
                - Pay-Per-Click (PPC) Advertising: Paying for ads on a cost-per-click basis
                - Analytics: Measuring and analyzing digital marketing campaigns and user behavior
                - Conversion Rate Optimization: Improving the percentage of visitors who take desired actions
                
                Digital marketing requires understanding customer behavior, creating engaging content,
                utilizing appropriate channels, and continuously analyzing performance metrics.
            """,

            "graphic design": """
                Graphic Design is the art and practice of planning and projecting ideas and experiences with
                visual and textual content. It combines typography, imagery, color theory, and page layout
                techniques to create visual compositions for various media.
                
                Key aspects of graphic design:
                
                - Visual Communication: Conveying messages and ideas through visual elements
                - Typography: Selection and arrangement of type for readability and aesthetic appeal
                - Color Theory: Understanding how colors interact and affect perception
                - Layout Design: Organizing visual elements effectively within a space
                - Logo and Brand Identity: Creating distinctive visual representations for brands
                - User Interface (UI) Design: Designing interfaces for digital products
                - Print Design: Creating materials for physical reproduction (posters, brochures, etc.)
                
                Graphic designers use software tools like Adobe Photoshop, Illustrator, and InDesign,
                or alternatives like Figma, Sketch, and Canva to bring their creative visions to life.
            """
        }


    # what to do next


    def get_base64_gif(self, gif_path):
        with open(gif_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    
    def display_chat_interface(self):
        st.title("🤖 Course Recommendation Chatbot")
        st.subheader("Ask me about courses or get personalized recommendations")

        # Add Clear Chat button to sidebar
        with st.sidebar:
            st.title("Options")
            if st.button("Clear Chat History"):
                self.clear_chat_history()

        # Display animated chatbot GIF when no messages have been exchanged
        if not st.session_state['past'] and not st.session_state['initial_message_shown']:
            try:
                # Try to locate and load the GIF (assuming there's an 'image' folder in the same directory)
                image_folder = os.path.join(os.path.dirname(__file__), 'image')
                gif_path = os.path.join(image_folder, 'data/image/Graphic_Design.gif')
                
                # Check if file exists
                if os.path.exists(gif_path):
                    encoded_gif = self.get_base64_gif(gif_path)
                    
                    # Display GIF with welcome message
                    st.markdown(f"""
                        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column; margin-bottom: 30px;">
                            <img src='data:image/gif;base64,{encoded_gif}' style='width: 250px; margin-bottom: 20px;'>
                            <div style="text-align:center; padding:10px 20px; font-size:18px; background-color: #f0f2f6; border-radius: 10px; max-width: 80%;">
                                Hello! I'm your course recommendation assistant. Ask me about Udemy courses or get personalized recommendations!
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Fallback to text-only welcome message
                    st.markdown("""
                        <div style="text-align:center; padding:20px; font-size:18px;">
                            I'm here to help you find the right courses. Try asking for recommendations in a specific area like 'Python programming' or 'digital marketing', or ask about course details like pricing or certificates.
                        </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading chatbot GIF: {e}")
                # Fallback to text-only welcome message
                st.markdown("""
                    <div style="text-align:center; padding:20px; font-size:18px;">
                        I'm here to help you find the right courses. Try asking for recommendations in a specific area like 'Python programming' or 'digital marketing', or ask about course details like pricing or certificates.
                    </div>
                """, unsafe_allow_html=True)

        # Chat interface
        user_input = st.text_input("Ask me about Udemy courses:", key="user_input", placeholder="e.g., Recommend Python courses for beginners")
        
        if user_input:
            self.process_input(user_input)
            st.session_state['initial_message_shown'] = True  # Hide initial message after input

        # Chat display
        self.display_chat()

    def clear_chat_history(self):
        """Clear all chat history from session state"""
        st.session_state['generated'] = []
        st.session_state['past'] = []
        st.session_state['chat_history'] = []
        st.session_state['recommendations'] = []
        st.session_state['initial_message_shown'] = False  # Reset welcome display
        st.rerun()

    def process_input(self, user_input):
        st.session_state.past.append(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        response = self.generate_response(user_input)
        st.session_state.generated.append(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    def generate_response(self, user_input):
        user_input_lower = user_input.lower()

        # Handle greeting
        if any(greeting in user_input_lower for greeting in ["hello", "hi", "hey", "greetings"]):
            return random.choice(["Hello! How can I help you today?", "Hi there! Looking for course recommendations?"])

        # Handle farewell
        if any(farewell in user_input_lower for farewell in ["bye", "goodbye", "see you", "thanks"]):
            return random.choice(["Goodbye!", "Thanks for chatting!"])
        
        if "roadmap" in user_input_lower:
            subject = self.extract_subject(user_input_lower)
            if subject:
                explanation = self.get_topic_explanation(subject)
                roadmap = self.get_roadmap(subject)
                if roadmap:
                    st.session_state['display_roadmap']=True
                    st.session_state['current_roadmap']=roadmap
                    return f"Here's a roadmap for learning {subject}:\n\n{explanation.strip() if explanation else 'No detailed explnantion available'}\n\nBelow is a suggested learning roadmap."
                else:
                    return f"Sorry, i don't have a roadmap for {subject} yet."
                
            else:
                return "Please specify a topic you'd like the roadmap for."
            

        if any(keyword in user_input_lower for keyword in ["what is", "explain","introduction to "]):
            subject = self.extract_subject(user_input_lower)
            if subject:
                explanation = self.get_topic_explanation(subject)
                if explanation:
                    return f"Here's a brief explanation of **{subject}**:\n\n{explanation.strip()}" 
                else:
                    return f"Sorry, I couldn't find a theoreticaloverview for {subject}."
            else:
                return "Please mention the topic you want to learn about."
        # Check for course recommendations

        if "recommend" in user_input_lower or "course" in user_input_lower:
            subject = self.extract_subject(user_input_lower)
            if subject:
                if self.course_data is not None:
                    # Search for a course that matches the subject
                    potential_courses = self.course_data[self.course_data['course_title'].str.contains(subject, case=False)]
                    
                    if not potential_courses.empty:
                        # Get the first matching course title to use for recommendations
                        course_title = potential_courses.iloc[0]['course_title']
                        recommendations = self.get_recommendation(course_title)
                        
                        st.session_state['recommendations'] = recommendations
                        return f"I've found some great courses similar to '{course_title}'! Here are my top recommendations based on content similarity."
                    else:
                        # If no exact match, search in course descriptions or provide generic recommendations
                        broader_search = self.course_data[
                            self.course_data['course_description'].str.contains(subject, case=False) | 
                            self.course_data['subject'].str.contains(subject, case=False)
                        ]
                        if not broader_search.empty:
                            st.session_state['recommendations'] = broader_search.head(6).to_dict(orient='records')
                            return f"I've found some courses related to {subject}! Here are some options that might interest you."
                
                # Fallback to basic recommendations
                basic_recs = self.get_basic_recommendations(subject)
                st.session_state['recommendations'] = basic_recs
                return f"I've found some courses on {subject}! Here are my recommendations based on ratings and popularity."
            else:
                return "Please specify a subject like 'Buisness Finance' or 'Web development'."

        return "I'm here to help you find the right courses. Try asking for recommendations in a specific area like 'Python programming' or 'digital marketing', or ask about course details like pricing or certificates."


    def recommend_courses(self,subject):
        if self.course_data is not None:
            potential_courses = self.course_data[self.course_data['course_title'].str.contains(subject, case=False)]
            if not potential_courses.empty:
                course_title = potential_courses.iloc[0]['course_title']
                st.session_state['recommendations'] = self.get_recommendation(course_title)
                return f"I've found some great courses similar to '{course_title}'! Here are my top recommendations based on content similarity."
            st.session_state['recommendations'] = self.get_basic_recommendations(subject)
            return f"Here are some courses on **{subject}** that might interest you."
            
    def get_basic_recommendations(self, subject, n=6):
        """Simple recommendation based on filtering and sorting"""
        if self.course_data is not None:
            filtered_courses = self.course_data[self.course_data['course_title'].str.contains(subject, case=False)]
            sorted_courses = filtered_courses.sort_values(by=['rating', 'num_subscribers'], ascending=False)
            return sorted_courses.head(n).to_dict(orient='records')
        
        # Include default image URL in sample data
        return [{
            'course_title': f"Sample Course on {subject}", 
            'rating': 4.5, 
            'num_subscribers': 1000, 
            'level': 'Beginner', 
            'url': '#',
            'image_url': '/api/placeholder/400/225'  # Default placeholder image
        }]

    def vectorize_text_to_cosine(self, df):
        """Create a cosine similarity matrix from course data"""
        # Create a combined feature column for vectorization
        temp_df = df.copy()
        temp_df['combined_features'] = temp_df['course_title'].fillna('') + " " + \
                                   temp_df['subject'].fillna('') + " " + \
                                   temp_df['level'].fillna('') + " " + \
                                   temp_df['course_description'].fillna('')
        
        # Vectorize and calculate cosine similarity
        count_vect = CountVectorizer(stop_words='english')
        cv_mat = count_vect.fit_transform(temp_df['combined_features'])
        cosine_sim_mat = cosine_similarity(cv_mat)
        return cosine_sim_mat

    def get_recommendation(self, title, num_of_rec=6):
        """Get recommendations based on course title using cosine similarity"""
        if self.course_data is None:
            return self.get_basic_recommendations(title)
        
        # Create a series mapping course titles to indices
        course_indices = pd.Series(self.course_data.index, index=self.course_data['course_title']).drop_duplicates()
        
        # Find the index of the course that matches the title
        if title not in course_indices:
            return self.get_basic_recommendations(title)
            
        idx = course_indices[title]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.cosine_sim_mat[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get the indices of the most similar courses (skipping the first which is the course itself)
        selected_indices = [i[0] for i in sim_scores[1:num_of_rec+1]]
        
        # Return the most similar courses
        result_df = self.course_data.iloc[selected_indices].copy()
        return result_df.to_dict(orient='records')

    def extract_subject(self, text):
        """Extract potential subject from user query"""
        common_subjects = ["python", "javascript", "web development", "data science", 
                         "machine learning", "marketing", "business", "design", 
                         "photography", "music", "art", "finance", "accounting",
                         "html", "css", "react", "node", "excel", "sql", "database"]
        
        # First check for exact matches of common subjects
        for subject in common_subjects:
            if subject in text:
                return subject
        
        # If no common subject found, extract potential keywords
        # Remove common words
        common_words = ["recommend", "course", "courses", "want", "looking", "for", "about", "me", "i", "need"]
        words = text.split()
        potential_subjects = [word for word in words if word not in common_words and len(word) > 2]
        
        if potential_subjects:
            return potential_subjects[0]  # Return the first potential subject
            
        return None

    def display_chat(self):
        # Display previous chats
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            st.markdown(f"**You:** {st.session_state['past'][i]}")
            st.markdown(f"**Assistant:** {st.session_state['generated'][i]}")

        if st.session_state['recommendations']:
            self.display_recommendations()
        if st.session_state['display_roadmap'] and st.session_state['current_roadmap']:
            self.display_roadmap(st.session_state['current_roadmap'])

    def display_recommendations(self):
        st.markdown("### 🎓 Recommended Courses")
        
        # CSS for cards with hover effect
        st.markdown("""
        <style>
        .course-card {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 10px 0;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .course-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 16px rgba(0, 0, 0, 0.2);
        }
        .course-image {
            width: 100%;
            height: 160px;
            object-fit: cover;
        }
        .course-content {
            padding: 15px;
        }
        .rating-star {
            color: #f9a825;
        }
        .enroll-button {
            background-color: #fffff;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            text-decoration: none;
            display: inline-block;
            font-weight: bold;
            margin-top: 10px;
            transition: background-color 0.3s ease;
        }
        .enroll-button:hover {
            background-color: #45a049;
        }
        .course-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Define HTML template for course cards
        CARD_TEMPLATE = """
        <div class="course-card">
            <img src="{image_url}" alt="{title}" class="course-image">
            <div class="course-content">
                <h4>{title}</h4>
                <p><span class="rating-star">★</span> {rating} ({num_subscribers} students)</p>
                <p>{level_display}</p>
                {price_display}
                <a href="{url}" target="_blank" class="enroll-button">Enroll Now</a>
            </div>
        </div>
        """
        
        # Create a grid layout for cards
        st.markdown('<div class="course-grid">', unsafe_allow_html=True)
        
        for course in st.session_state['recommendations']:
            title = course.get('course_title', course.get('title', 'Course Title'))
            # Truncate title if too long
            if len(title) > 60:
                title = title[:57] + "..."
                
            rating = course.get('rating', 'N/A')
            subscribers = course.get('num_subscribers', 'N/A')
            level = course.get('level', 'All Levels')
            
            # Handle price display
            price = course.get('price', 'N/A')
            price_display = f'<p><strong>Price:</strong> {price}</p>' if price != 'N/A' else ''
            
            # Handle level display
            level_display = f'<strong>Level:</strong> {level}' if level != 'N/A' else ''
            
            # Include URL with fallback
            url = course.get('url', '#')
            if url == '' or url is None:
                url = '#'
                
            # Include image URL with fallback
            image_url = course.get('image_url', '/api/placeholder/400/225')
            if image_url == '' or image_url is None:
                image_url = '/api/placeholder/400/225'  # Placeholder image
            
            card_html = CARD_TEMPLATE.format(
                title=title,
                rating=rating,
                num_subscribers=subscribers,
                level_display=level_display,
                price_display=price_display,
                url=url,
                image_url=image_url
            )
            
            st.markdown(card_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# To run the chatbot
def display_chat_interface(course_data=None):
    chatbot = ChatBot(course_data)
    chatbot.display_chat_interface()

if __name__ == "__main__":
    display_chat_interface()  # Just call with course data if you have it