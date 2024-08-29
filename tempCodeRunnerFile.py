response = self.llm(prompt=self.prompt_template.format(context=context, question=msg_dict['content']))
            print(response)