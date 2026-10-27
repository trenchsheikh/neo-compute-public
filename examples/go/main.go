package main

import (
 "encoding/json"
 "fmt"
 "net/http"
 "net/url"
 "time"
)

type Offer struct { Provider string `json:"provider"`; GPU string `json:"gpu"`; Hourly float64 `json:"hourly"`; Region string `json:"region"` }
type Response struct { Connected bool `json:"connected"`; Offers []Offer `json:"offers"`; Notice string `json:"notice"` }

func main() {
 client := &http.Client{Timeout: 10 * time.Second}
 endpoint := "https://neo-compute.vercel.app/api/offers?gpu=" + url.QueryEscape("H100")
 resp, err := client.Get(endpoint); if err != nil { panic(err) }; defer resp.Body.Close()
 if resp.StatusCode != http.StatusOK { panic(fmt.Sprintf("upstream status %d",resp.StatusCode)) }
 var data Response; if err := json.NewDecoder(resp.Body).Decode(&data); err != nil { panic(err) }
 if !data.Connected { fmt.Println("Unavailable:", data.Notice); return }
 for _, offer := range data.Offers { fmt.Printf("%s: %s $%.2f/GPU-hour (%s)\n",offer.Provider,offer.GPU,offer.Hourly,offer.Region) }
}
