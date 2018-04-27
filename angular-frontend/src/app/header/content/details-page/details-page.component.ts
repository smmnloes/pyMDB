import {Component, OnInit} from '@angular/core';
import {DetailService} from "../../../detail.service";
import {HttpClient} from "@angular/common/http";
import {CombinedDataModel} from "../search-page/search-results/result/combined-data-model";
import {Subject} from "rxjs/Subject";

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.css']
})
export class DetailsPageComponent implements OnInit {
  private combinedData: CombinedDataModel;

  private fullPosterPathSource = new Subject<String>();
  private fullPosterPath$ = this.fullPosterPathSource.asObservable();

  constructor(private detailService: DetailService, private http: HttpClient) {
  }

  ngOnInit() {
    this.detailService.combinedData$.subscribe(combinedData => {
      this.combinedData = combinedData;
      console.log(combinedData);
      if (this.hasPosterPath()) {
        this.getFullPosterPath();
      }
    })
  }

  private hasDetailData() {
    return this.combinedData.detailedData != null;
  }

  private hasPosterPath() {
    return this.hasDetailData() && this.combinedData.detailedData.posterPath != null;
  }


  /*
  Poster sizes:
   "w92",
   "w154",
   "w185",
   "w342",
   "w500",
   "w780",
   "original"
   */

  private getFullPosterPath() {
    return this.http.get(this.detailService.TMDB_ROOT + 'configuration?api_key=' + this.detailService.TMDB_API_KEY).subscribe(configData => {
        let baseUrl = configData['images']['base_url'];
        this.fullPosterPathSource.next(baseUrl + 'w185' + this.combinedData.detailedData.posterPath);
      }
    );

  }

}
