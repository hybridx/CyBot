# Chatbot Application
<table>
<tr>
<td>
   A chatbot application using RasaNLU to have a general conversation as well as customized replies.
</table>
</tr>
</td>

### You can check it out here!

Website: https://www.cybzilla.com

### Development
Here's what you need to know about the API endpoints

 - @create - `/app/data/create`
 - @set - `/app/data/update`
 - @remove - `/app/data/remove`
 - @read - `/app/data/get_intent_data`
 	   `/app/data/read_all_intents`

##### The request data needs to be in the following format

```
data
{
	"intent":<>,
	"username":<>,
	"answers":[],
	"questions":[]
}
```

