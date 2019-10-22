import {Component, Input, OnInit} from '@angular/core';
import {BasicDataModel} from "./basic-data-model";
import {DetailService} from "../../../../../services/detail.service";
import {Router} from "@angular/router";
import {ToastrService} from "ngx-toastr";
import {first} from "rxjs/operators";


@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  @Input()
  basicData: BasicDataModel;


  constructor(private detailService: DetailService, private router: Router, private toastrService: ToastrService) {
  }

  ngOnInit() {
  }

  goToDetails() {
    this.detailService.detailedData$.pipe(first()).subscribe(data =>
      data.hasDetails ?
        this.router.navigate(["/details", this.basicData.tid])
        :
        this.toastrService.warning("No detailed data available"));
    this.detailService.getDetails(this.basicData.tid);
  }

}
