export class Client{
	constructor(a){
		this._s=new WebSocket("ws://"+a[0]+":"+a[1]+"/")
		this._s.onopen=this.on_connect
		this._s.onclose=this.on_close
		this._s.onmessage=this._m
		this._s.onerror=this.on_error
		this._a=a
		this.packets={}
	}
	on_connect(){
		document.body.innerHTML="Connected!"
	}
	on_close(){
		document.body.innerHTML="Disconnected :("
	}
	on_error(e){
		console.warn(e)
		e.stopImmediatePropagation()
		e.stopPropagation()
		e.preventDefault()
	}
	_m(m){
		if (m=="null"):return
		var k=m.split(":")[0]
		var v=m.substring(k.length+1)
		if (!Object.keys(this.packets).includes(k)){
			this.on_error("Invalid packet!")
			return
		}
	 	var r=this.packets[k](v)
	 	if (r!="null"){
	 		this.send(r)
	 	}
	}
	packets(){
		return this.packets
	}
	add_packet(k,v){
		this.packets[k]=v
	}
}