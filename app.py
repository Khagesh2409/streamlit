import streamlit as st
from key import OPENAI_API_KEY

def modelfunc(temp_text, case_text, option):
	switchtemplate = {
		"Suit for Permanent Injunction": "You are a lawyer. This is a template of SUIT FOR DECLARATION AND PERMANENT INJUCTION.\n\n",
		"Will": "You are a lawyer. This is a template of a will.\n\n"
	}
	switchcase = {
		"Suit for Permanent Injunction": "These are the case notes for a SUIT FOR DECLARATION AND PERMANENT INJUCTION. I want you to use these case notes to fill the given template with necessary data like user information extracted from these case notes. Generate necessary clauses with sufficient data elaborating the situation behind the cause of the case being filed.\n\n",
		"Will": "These are the case notes for a new will. I want you to use these case notes to fill the given template with necessary data like user information extracted from these case notes."
	}
	
	
	templatetext = switchtemplate.get(option, "You are a lawyer. This is a templte.\n\n") + temp_text
	casenotes = switchcase.get(option, "These are the case notes. I want you to use these case notes to fill the given template with necessary data like user information extracted from these case notes.\n\n") + case_text

	response = client.chat.completions.create(
	model="gpt-3.5-turbo-16k",
	messages=[
  	{
      	"role": "system",
	"content": templatetext 
	},
	{
	"role": "user",
	"content": casenotes
	}
	],
	temperature=1,
	max_tokens=12384,
  	top_p=1,
  	frequency_penalty=0,
  	presence_penalty=0
	)	
	#generated_texts = [
        #response["choices"][0].message["content"]
    	#]
	#return generated_texts
	return response.choices[0].message.content


# Page title
st.set_page_config(page_title='DraftAI')
st.title('Draft:blue[AI]')

st.image('draftailogo.png', width=140)
#st.markdown("<h1 style='text-align: center;'>Draft<font color=blue>AI</font></h1>", unsafe_allow_html=True)


option = st.selectbox(
   "What type of draft are you working on?",
   ("Suit for Permanent Injunction", "Will", "Contract", "Plaint", "WS", "Other"),
   index=None,
   placeholder="Type of Legal Document",
)

# Template text
#temp_text = st.text_input('Enter your template:', placeholder = 'Template')

# Query text
#case_text = st.text_input('Enter your case notes:', placeholder = 'Case Notes')

# Template upload
temp_file = st.file_uploader('Here goes your template', type='txt', disabled=not(option))

# Case notes upload
case_file = st.file_uploader('and insert case notes here', type='txt', disabled=not(option))

if (temp_file):
	temp_text = temp_file.read().decode()

if (case_file):
	case_text = case_file.read().decode()

# Form input and query
result = []
with st.form('myform', clear_on_submit=True):
	submitted = st.form_submit_button('Submit', disabled=not(case_file))
	if submitted:
		with st.spinner('Calculating...'):
			response = modelfunc(temp_text, case_text, option)
			result.append(response)

if len(result):
	st.write(response)

