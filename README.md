# Chatbot Application
<table>
<tr>
<td>
   A chatbot application using RasaNLU to have a general conversation as well as customized replies.
</table>
</tr>
</td>

### You can check it out here!

Website: https://aitechbay.com

### Development
Here's what you need to know about the API endpoints

 - @create - `/api/data/create`
 - @set - `/api/data/update`
 - @remove - `/api/data/remove`
 - @read - `/api/data/{}`

##### The data needs to be in the following format

```
data
{
	"intent":<>,
	"username":<>,
	"answers":[],
	"questions":[]
}
```

