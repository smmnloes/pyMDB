import {Component, Input, OnInit} from '@angular/core';
import {BasicDataModel} from "./basic-data-model";
import {DetailService} from "../../../../../services/detail.service";
import {Router} from "@angular/router";
import {ToastrService} from "ngx-toastr";
import {first} from "rxjs/operators";
import {DetailedDataModel} from "./detailed-data-model";


@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  @Input()
  basicData: BasicDataModel;

  @Input()
  activateTitleLink: boolean;

  constructor(private detailService: DetailService, private router: Router, private toastrService: ToastrService) {
  }

  ngOnInit() {
  }

  goToDetails() {
    this.detailService.getDetails(this.basicData.tid).pipe(first()).subscribe(
      (detailedData: DetailedDataModel) =>
        this.router.navigate(["/details", this.basicData.tid], {
          state: {
            basicData: this.basicData,
            detailedData: detailedData
          }
        }),
      error => {
        switch (error.status) {
          case 404:
            this.toastrService.warning("No detailed data available");
            break;
          case 500:
            this.toastrService.error("Internal Error, try again later")
            break;
        }
      }
    );
  }

}
