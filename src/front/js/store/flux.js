const getState = ({ getStore, getActions, setStore }) => {
    return {
        store: {
            message: null,
            demo: [
                {
                    title: "FIRST",
                    background: "white",
                    initial: "white"
                },
                {
                    title: "SECOND",
                    background: "white",
                    initial: "white"
                }
            ]
        },


























































































        
        actions: {
            obtenerEventos: async ()=> {
                try {
                    const res = await fetch(process.env.BACKEND_URL+"/api/events")
                    const data = await res.json()
                    setStore({events:data.result})
                    
                } catch (error) {
                    console.error(error) 
                }               
                    
                    
            },
            login: async (email, password) => {

				try {
					let response = await fetch("https://shiny-dollop-qgq7xr79pxg24747-3001.app.github.dev/api/login", {
						method:"POST",
						headers: {
							"Content-type":"application/json"
						},
						body: JSON.stringify({
							"email": email,
							"password": password
						})
					});

					let data = await response.json();
					localStorage.setItem("token",data);
						return true;
				} catch (error) {
					console.log(error);
						return false;
				}
            }
        }
    };
};
export default getState;